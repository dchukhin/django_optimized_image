import factory
import factory.fuzzy

from optimized_image.fields import OptimizedImageField


class GenericModelFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(length=8)
    image = factory.django.ImageField(filename="image.png")
    not_optimized_image = factory.django.ImageField(filename="image2.png")
    not_optimized_image_ignored = factory.django.ImageField(filename="ignore-me.gif")

    class Meta:
        model = 'not_optimized.GenericModel'


class BlogPostOrSomethingFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(length=8)
    image1 = factory.django.ImageField(filename="image1.png")
    image2 = factory.django.ImageField(filename="image2.png")
    not_optimized_image_ignored = factory.django.ImageField(filename="ignore-me.gif")

    class Meta:
        model = 'not_optimized.BlogPostOrSomething'
