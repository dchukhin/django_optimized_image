from django.apps import apps

from .models import OptimizedNotOptimized


def get_optimized_url(model_instance, field_name):
    """Returns the optimized url for an instance of a model and a field name."""
    optimized_data = OptimizedNotOptimized.objects.get(
        instance_model=model_instance._meta.label,
        instance_pk=model_instance.pk,
        field_name=getattr(model_instance, field_name).field.attname
    )
    return optimized_data.optimized_url
