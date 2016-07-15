from django.db import models

# Create your models here.


class BlogPostOrSomething(models.Model):
    title = models.CharField(max_length=255)
    image1 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image2 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image3 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image4 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image5 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image6 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image7 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image8 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image9 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image10 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image11 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image12 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image13 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image14 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image15 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
    image16 = models.ImageField(blank=True, null=True, upload_to='optimized-images/')
