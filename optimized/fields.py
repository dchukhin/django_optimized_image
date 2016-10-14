import tinify

from django.conf import settings
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile


class OptimizedImageFieldFile(ImageFieldFile):

    @property
    def optimized_url(self):
        self._require_file()
        from .utils import get_optimized_url
        return get_optimized_url(self.instance, self.field.name)

    def delete(self, save=True):
        """Remove the OptimizedNotOptimized object on image deletion."""
        from .models import OptimizedNotOptimized
        optimized_data_obj = OptimizedNotOptimized.objects.filter(
            instance_model=self.instance._meta.label,
            instance_pk=self.instance.pk,
            field_name=self.field.name
            )
        super().delete(save)
        if optimized_data_obj.exists():
            optimized_data_obj[0].delete()



class OptimizedImageField(ImageField):
    """An ImageField that gets optimized on save() using tinyPNG."""
    attr_class = OptimizedImageFieldFile

    def pre_save(self, model_instance, add):
        """Optimize the image being saved and create an instance in db linking to the image."""
        image_file = getattr(model_instance, self.name)
        # Has this image been saved?
        if not image_file._committed:
            # The image is being saved now, so we optimize it
            s3_response = save_to_s3(image_file)

            # Add checking in here?
            from .models import OptimizedNotOptimized
            new_object, created = OptimizedNotOptimized.objects.get_or_create(
                instance_model=model_instance._meta.label,
                instance_pk=model_instance.pk,
                field_name=self.name,
            )
            new_object.url = getattr(model_instance, self.name)
            new_object.optimized_url = s3_response.location
            new_object.save()
        return super().pre_save(model_instance, add)

    def save_form_data(self, instance, data):
        """Remove the OptimizedNotOptimized object on clearing the image."""
        from .models import OptimizedNotOptimized
        # If we are clearing the image
        if data == False:
            optimized_data_obj = OptimizedNotOptimized.objects.filter(
                instance_model=instance._meta.label,
                instance_pk=instance.pk,
                field_name=self.name
            )
            if optimized_data_obj.exists():
                optimized_data_obj[0].delete()
        super().save_form_data(instance, data)

def save_to_s3(image_file):
    tinify.key = settings.TINYPNG_KEY
    source = tinify.from_file(image_file)
    # Save to s3
    s3_response = source.store(
        service="s3",
        aws_access_key_id=settings.S3_KEY_ID,
        aws_secret_access_key=settings.S3_ACCESS_KEY,
        region=settings.S3_REGION,
        path="{}/{}{}".format(
            settings.S3_BUCKET,
            settings.S3_OPTIMIZED_IMAGES_FOLDER,
            image_file.name)
    )
    return s3_response
