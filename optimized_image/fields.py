import tinify

from django.conf import settings
from django.db.models import ImageField


class OptimizedImageField(ImageField):
    """An ImageField that gets optimized on save() using tinyPNG."""
    def save_form_data(self, instance, data):
        """Remove the OptimizedNotOptimized object on clearing the image."""
        # Are we updating an image?
        updating_image = True if data and getattr(instance, self.name) != data else False

        if updating_image:
            data = optimize_from_buffer(data)
            super().save_form_data(instance, data)


def optimize_from_buffer(data):
    """Optimize an image that has not been saved to a file."""
    from .utils import is_testing_mode
    if not is_testing_mode():
        tinify.key = settings.TINYPNG_KEY
        optimized_buffer = tinify.from_buffer(data.file.read()).to_buffer()
        data.seek(0)
        data.file.write(optimized_buffer)
        data.file.truncate()
    return data


def save_to_s3(image_file, image_name):
    from .utils import is_testing_mode
    if not is_testing_mode:
        try:
            tinify.key = settings.TINYPNG_KEY
            source = tinify.from_file(image_file)
            # Save to s3
            s3_response = source.store(
                service="s3",
                aws_access_key_id=settings.S3_KEY_ID,
                aws_secret_access_key=settings.S3_ACCESS_KEY,
                region=settings.S3_REGION,
                path="{}/{}{}".format(
                    settings.S3_BUCKET,
                    settings.S3_OPTIMIZED_IMAGES_FOLDER,
                    image_name)
            )
        except tinify.errors.Error as tinify_error:
            class s3response(object):
                height = 0
                width = 0
                location = ''
                error = tinify_error
            s3_response = s3response()
            # s3_response = {'error:': error, 'location': ''}
    else:
        class s3response(object):
            height = image_file.height
            width = image_file.width
            location = image_file.name
            error = ''
        s3_response = s3response()
    return s3_response
