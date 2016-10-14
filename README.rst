==============
Django-tinypng
==============

Django-tinypng is a simple Django library to allows optimization
of images by using TinyPNG. Saving an image locally to an
OptimizedImageField uses TinyPNG to optimize the image, then S3
to store it.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "optimized" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'optimized',
    ]

2. Add the following settings to your settings file. Note: it is a
   good idea to keep most, if not all, of these secret::

    TINYPNG_KEY
    S3_KEY_ID 
    S3_ACCESS_KEY
    S3_REGION
    S3_BUCKET
    S3_OPTIMIZED_IMAGES_FOLDER

3. Run `python manage.py migrate` to create the optimized models.

4. You may use the `OptimizedImageField` by importing it::


    from optimized.fields import OptimizedImageField

   and saving images into it, the same way you would to a Django `ImageField`.

5. You may get an optimized url by using the `get_optimized_url` function
   for an instance of an object. For a blogpost with an `image` field that
   has had an image uploaded you may run::

    from optimized.utils import get_optimized_url
    get_optimized_url(blogpost, ‘image’)
