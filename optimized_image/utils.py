from io import BytesIO
from PIL import Image
import os
import sys
import tinify

from django.conf import settings
from django.core.files.base import ContentFile

from .fields import OptimizedImageField


def optimize_from_buffer(data):
    """Optimize an image that has not been saved to a file."""
    # NOTE: this optional setting defines image file extensions that should
    # be ignored during optimization. If it is not set or is set to an
    # empty list, all file types will be optimized.
    IGNORED_EXTENSIONS = getattr(settings, 'OPTIMIZED_IMAGE_IGNORE_EXTENSIONS', [])
    if not is_testing_mode():
        base_extension = data.name.split('.')[-1]

        # If this file's extension is in the list of file extensions
        # that should be ignored, just return the data unmodified,
        # the same as we do if ``is_testing_mode()`` is True.
        if base_extension.lower() in [ext.lower() for ext in IGNORED_EXTENSIONS]:
            return data

        if settings.OPTIMIZED_IMAGE_METHOD == 'pillow':
            image = Image.open(data)
            bytes_io = BytesIO()
            if base_extension.lower() != 'jpg':
                extension = base_extension.upper()
            else:
                extension = 'JPEG'
            image.save(bytes_io, format=extension, optimize=True)
            data.seek(0)
            data.file.write(bytes_io.getvalue())
            data.file.truncate()
        elif settings.OPTIMIZED_IMAGE_METHOD == 'tinypng':
            tinify.key = settings.TINYPNG_KEY
            optimized_buffer = tinify.from_buffer(data.file.read()).to_buffer()
            data.seek(0)
            data.file.write(optimized_buffer)
            data.file.truncate()
    return data


def optimize_legacy_images_in_model_fields(list_of_models, verbosity=0):
    """
    Call this function to go through models and optimize images.

    This is best done after changing your model fields from ImageField to
    OptimizedImageField, and migrating the models. This function goes through
    the list_of_models in the params, finds all of their OptimizedImageFields,
    and optimizes the images in those fields. Note: there is a 500 image/month
    limit on a free TinyPNG API key, so use this function wisely.
    """
    # NOTE: this optional setting defines image file extensions that should
    # be ignored during optimization. If it is not set or is set to an
    # empty list, all file types will be optimized.
    IGNORED_EXTENSIONS = getattr(settings, 'OPTIMIZED_IMAGE_IGNORE_EXTENSIONS', [])
    for model in list_of_models:
        if verbosity == 1:
            sys.stdout.write('\nOptimizing for model: {}'.format(model))

        field_names_to_optimize = []
        for field in model._meta.get_fields():
            if type(field) == OptimizedImageField:
                field_names_to_optimize.append(field.attname)

        if verbosity == 1:
            sys.stdout.write('\nWill check the following fields: {}'.format(field_names_to_optimize))

        model_instances = model.objects.all()
        for model_instance in model_instances:
            for field_name in field_names_to_optimize:
                if verbosity == 1:
                    sys.stdout.write('\nChecking for instance id {} field {}'.format(model_instance.pk, field_name))

                # If the instance's field has an image, optimize it
                image_file = getattr(model_instance, field_name)
                image_file_extension = image_file.name.split('.')[-1]

                # If the file extension is in the list of file extensions
                # that should be ignored for optimization, exit this iteration
                # of the inner ``for`` loop, skipping the file.
                if image_file_extension.lower() in [ext.lower() for ext in IGNORED_EXTENSIONS]:
                    sys.stdout.write(
                        '\nImage has extension {ext}. Ignoring.'.format(ext=image_file_extension)
                    )
                    continue

                if image_file.name not in [None, '']:
                    if verbosity == 1:
                        sys.stdout.write('\nImage found. Optimizing.')

                    try:
                        # Use the OPTIMIZED_IMAGE_METHOD from settings to determine
                        # which way to optimize the image file.
                        if settings.OPTIMIZED_IMAGE_METHOD == 'pillow':
                            # Open the image
                            input_file = BytesIO(image_file.read())
                            image = Image.open(input_file)
                            output_file = BytesIO()
                            # Find the extension of the file to pass to PIL.Image.save()
                            if image_file_extension.lower() != 'jpg':
                                extension = image_file_extension.upper()
                            else:
                                extension = 'JPEG'
                            # Optimize the image
                            image.save(output_file, format=extension, optimize=True)
                            # Save the image in place of the unoptimized one
                            content_file = ContentFile(output_file.getvalue())
                            image_name = os.path.relpath(image_file.name, image_file.field.upload_to)
                            image_file.save(image_name, content_file)
                        elif settings.OPTIMIZED_IMAGE_METHOD == 'tinypng':
                            tinify.key = settings.TINYPNG_KEY
                            # Use TinyPNG to optimize the file from a buffer
                            optimized_buffer = tinify.from_buffer(image_file.read()).to_buffer()
                            # Save the image in place of the unoptimized one
                            content_file = ContentFile(optimized_buffer)
                            image_name = os.path.relpath(image_file.name, image_file.field.upload_to)
                            image_file.save(image_name, content_file)
                    except:
                        # If the optimization failed for any reason, write this
                        # to stdout.
                        sys.stdout.write('\nOptimization failed for {}.'.format(image_file.name))

                    if verbosity == 1:
                        sys.stdout.write('\nOptimized and saved image.')


def is_testing_mode():
    """Return True if currently running tests."""
    return True if 'test' in sys.argv else False
