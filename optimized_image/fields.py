import tinify

from django.conf import settings
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile


class OptimizedImageFieldFile(ImageFieldFile):

    @property
    def optimized_url(self):
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

    def save(self, name, content, save=True):
        """Update the OptimizedNotOptimized object every time an image is saved."""
        from optimized_image.models import OptimizedNotOptimized
        super().save(name, content, save)

        self.instance.save()

        # Create an OptimizedNotOptimized object for this image
        new_object, created = OptimizedNotOptimized.objects.get_or_create(
            instance_model=self.instance._meta.label,
            instance_pk=self.instance.pk,
            field_name=self.field.attname,
        )

        # If we are keeping the original image, then save it to s3, and update
        # the OptimizedNotOptimized object.
        if self.field.keep_original:
            if created or not new_object.optimized_url.endswith(content.name):
                s3_response = save_to_s3(content.file, content.name)
                # Set the new_object url and optimized_url
                new_object.url = content.url
                new_object.optimized_url = s3_response.location
                new_object.save()
        else:
            # We are not keeping the original image, so just update the
            # OptimizedNotOptimized object with the url.
            new_object.optimized_url = self.url
            new_object.save()


class OptimizedImageField(ImageField):
    """An ImageField that gets optimized on save() using tinyPNG."""
    def __init__(self, keep_original=False, **kwargs):
        """Set self.keep_original based on arguments that are passed in."""
        self.keep_original = keep_original
        super().__init__(**kwargs)

    attr_class = OptimizedImageFieldFile

    def save_form_data(self, instance, data):
        """Remove the OptimizedNotOptimized object on clearing the image."""
        from .models import OptimizedNotOptimized
        # If we are clearing the image
        if data is False:
            optimized_data_obj = OptimizedNotOptimized.objects.filter(
                instance_model=instance._meta.label,
                instance_pk=instance.pk,
                field_name=self.name
            )
            if optimized_data_obj.exists():
                optimized_data_obj[0].delete()

        # Are we updating an image?
        updating_image = True if data and getattr(instance, self.name) != data else False

        # If we're not keeping the original file (meaning that the new file will
        # override the file being uploaded), then optimize the file, and save it.
        if not self.keep_original:
            if updating_image:
                data = optimize_from_buffer(data)
                super().save_form_data(instance, data)
        else:
            # We're keeping the original file, and the optimized file
            super().save_form_data(instance, data)

            # Now that the save has occurred, optimize the image (if necessary)
            if updating_image:
                image_file = getattr(instance, self.name)
                # Update the image_file to have the correct name
                new_name = getattr(instance, self.name).field.upload_to + image_file.name
                image_file.name = new_name

                # Optimize the image
                s3_response = save_to_s3(data, new_name)

                # The OptimizedNotOptimized object
                # TODO: Add checking in here?
                from .models import OptimizedNotOptimized
                new_object, created = OptimizedNotOptimized.objects.get_or_create(
                    instance_model=instance._meta.label,
                    instance_pk=instance.pk,
                    field_name=self.name,
                )
                # Set the new_object url and optimized_url
                new_object.url = image_file.url
                new_object.optimized_url = s3_response.location
                new_object.save()


def optimize_from_buffer(data):
    """Optimize an image that has not been saved to a file."""
    tinify.key = settings.TINYPNG_KEY
    optimized_buffer = tinify.from_buffer(data.file.read()).to_buffer()
    data.seek(0)
    data.file.write(optimized_buffer)
    data.file.truncate()
    return data


def save_to_s3(image_file, image_name):
    try:
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
                image_name)
        )
    except tinify.errors.Error as tinify_error:
        class s3response(object):
            height = 0
            width = 0
            location = ''
            error = tinify_error
        s3_response = s3response()
        # s3_response = {'error:': error, 'location': ''}
    return s3_response
