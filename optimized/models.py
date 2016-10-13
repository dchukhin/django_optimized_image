from django.db import models

from .fields import OptimizedImageField


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






class OptimizedNotOptimized(models.Model):
    instance_model = models.CharField(max_length=100)
    instance_pk = models.IntegerField()
    field_name = models.CharField(max_length=100)
    url = models.URLField()
    optimized_url = models.URLField()

    def __str__(self):
        return "{} pk {} optimized field {}".format(self.instance_model, self.instance_pk, self.field_name)
