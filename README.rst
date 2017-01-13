======================
django-optimized-image
======================

django-optimized-image is a simple Django library to allows optimization
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

2. Because optimized_image uses TinyPNG and S3, you will need to
   get API keys from each of them. Visit https://tinypng.com/developers
   and http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html
   for more details on getting a TinyPNG API key (easy) and setting
   up an S3 bucket (harder). Once you have done so, add the
   following settings to your settings file. Note: it is a good idea
   to keep most, if not all, of these secret::

    TINYPNG_KEY # Go to
    S3_KEY_ID
    S3_ACCESS_KEY
    S3_REGION
    S3_BUCKET
    S3_OPTIMIZED_IMAGES_FOLDER

3. Migrate the optimized_image models::

    python manage.py migrate optimized_image

4. You may use the `OptimizedImageField` by importing it::


    from optimized_image.fields import OptimizedImageField

   and saving images into it, the same way you would to a Django `ImageField`.

5. You may get an optimized url by using the `get_optimized_url` function
   for an instance of an object. For a blogpost with an ``image`` field that
   has had an image uploaded you may run::

    from optimized_image.utils import get_optimized_url
    get_optimized_url(blogpost, ‘image’)

6. If you want to change legacy models with Django's Image fields and
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
