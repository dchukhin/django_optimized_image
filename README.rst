======================
django_optimized_image
======================

django_optimized_image is a simple Django library to allows optimization
of images by using TinyPNG. Saving an image locally to an
OptimizedImageField uses TinyPNG to optimize the image, then S3
to store it.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "optimized_image" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'optimized_image',
    ]

2. Because optimized_image uses TinyPNG, you will need to get an API key from
   TinyPNG. Visit https://tinypng.com/developers for more details on getting an
   API key. When images are uploaded, you will also have the option to keep the
   original (unoptimized) image. If you choose to do so, you will need to create
   an S3 bucket to upload the optimized images to.  You may visit
   http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html for more
   information on setting up an S3 bucket. Once you have done so, add the
   following settings to your settings file. Note: it is a good idea
   to keep most, if not all, of these secret::

    TINYPNG_KEY  # Required
    S3_KEY_ID  # Required if you want to keep original (unoptimized) images
    S3_ACCESS_KEY  # Required if you want to keep original (unoptimized) images
    S3_REGION  # Required if you want to keep original (unoptimized) images
    S3_BUCKET  # Required if you want to keep original (unoptimized) images
    S3_OPTIMIZED_IMAGES_FOLDER  # Required if you want to keep original (unoptimized) images

3. Migrate the optimized_image models::

    python manage.py migrate optimized_image

4. You may use the ``OptimizedImageField`` by importing it::


    from django.db import models

    from optimized_image.fields import OptimizedImageField


    class MyModel(models.Model):
        ...
        image = OptimizedImageField()

   and saving images into it, the same way you would to a Django ``ImageField``.
   The optimized image will be saved into the ``url`` field in place of the
   unoptimized image.

5. If you want to change legacy models with Django's Image fields and
   optimize the images in those fields, you may do so for legacy models
   by passing a list of legacy model classes (not their instances) to
   the following function::

    from optimized_image.utils import optimize_legacy_images_in_model_fields
    optimize_legacy_images_in_model_fields([LegacyModelClass1, LegacyModelClass2])

   Note: this function makes calls to TinyPNG and S3, so it can take a really
   long time, depending on how many images you have. You may pass in 1
   for the verbosity parameter to get logs on the progress::

    optimize_legacy_images_in_model_fields([LegacyModelClass1, LegacyModelClass2], verbosity=1)

 Note about TinyPNG API keys: If you obtain the free TinyPNG API token, you are limited to 500
 image optimizations per month, so this function may fail if you have a
 lot of images. You may either obtain a paid API key, or wait until next month.
