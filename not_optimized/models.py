from django.db import models

from optimized.fields import OptimizedImageField


class BlogPostOrSomething(models.Model):
    title = models.CharField(max_length=255)
    image1 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image2 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image3 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image4 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image5 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image6 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image7 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image8 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image9 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image10 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image11 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image12 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image13 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image14 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image15 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    image16 = OptimizedImageField(blank=True, null=True, upload_to='static/images/')


class GenericModel(models.Model):
    title = models.CharField(max_length=255)
    image = OptimizedImageField(blank=True, null=True, upload_to='static/images/')
    not_optimized_image = models.ImageField(blank=True, null=True, upload_to='static/images')
