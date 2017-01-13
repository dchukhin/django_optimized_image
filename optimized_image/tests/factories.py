import factory
import factory.fuzzy

from optimized_image.fields import OptimizedImageField


class OptimizedNotOptimizedFactory(factory.django.DjangoModelFactory):
    instance_model = factory.fuzzy.FuzzyText(length=8)
    instance_pk = factory.fuzzy.FuzzyInteger(low=1)
    field_name = factory.fuzzy.FuzzyText(length=8)
    url = factory.fuzzy.FuzzyText()
    optimized_url = factory.fuzzy.FuzzyText()

    class Meta:
        model = 'optimized_image.OptimizedNotOptimized'


class GenericModelFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(length=8)
    image = factory.django.ImageField(filename="image.png")
    not_optimized_image = factory.django.ImageField(filename="image2.png")

    class Meta:
        model = 'not_optimized.GenericModel'
