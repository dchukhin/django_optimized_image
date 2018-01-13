import factory
import factory.fuzzy

from optimized_image.fields import OptimizedImageField


class GenericModelFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(length=8)
    image = factory.django.ImageField(filename="image.png")
    not_optimized_image = factory.django.ImageField(filename="image2.png")

    class Meta:
        model = 'not_optimized.GenericModel'
