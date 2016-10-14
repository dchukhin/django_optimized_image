from django.apps import apps

from .fields import OptimizedImageField, save_to_s3
from .models import OptimizedNotOptimized


def get_optimized_url(model_instance, field_name):
    """Returns the optimized url for an instance of a model and a field name."""
    optimized_data = OptimizedNotOptimized.objects.filter(
        instance_model=model_instance._meta.label,
        instance_pk=model_instance.pk,
        field_name=getattr(model_instance, field_name).field.attname
    )
    if optimized_data.exists():
        return optimized_data[0].optimized_url
    return ''


def optimize_legacy_images_in_model_fields(list_of_models):
    """
    Call this function to go through models and optimize images.

    This is best done after changing your model fields from ImageField to
    OptimizedImageField, and migrating the models. This function goes through
    the list_of_models in the params, finds all of their OptimizedImageFields,
    and optimizes any that don't currently have a value for optimized_url.
    Note: there is a 500 image/month limit on a free TinyPNG API key, so
    use this function wisely.
    """
    for model in list_of_models:
        field_names_to_optimize = []
        for field in model._meta.get_fields():
            if type(field) == OptimizedImageField:
                field_names_to_optimize.append(field.attname)
        model_instances = model.objects.all()
        for model_instance in model_instances:
            for field_name in field_names_to_optimize:
                # If the instance's field has an image, but an optimized_url
                # equal to the empty string, optimize the image in that field
                image_file = getattr(model_instance, field_name)
                if image_file.name not in [None, ''] and getattr(model_instance, field_name).optimized_url == '':
                    s3_response = save_to_s3(image_file)
                    # Add checking in here?
                    new_object, created = OptimizedNotOptimized.objects.get_or_create(
                        instance_model=model_instance._meta.label,
                        instance_pk=model_instance.pk,
                        field_name=field_name,
                    )
                    new_object.url = image_file.name
                    new_object.optimized_url = s3_response.location
                    new_object.save()
