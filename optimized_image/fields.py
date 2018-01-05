from io import BytesIO
from PIL import Image
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
        if settings.OPTIMIZED_IMAGE_METHOD == 'pillow':
            image = Image.open(data)
            bytes_io = BytesIO()
            if data.name.split('.')[-1].lower() != 'jpg':
                extension = data.name.split('.')[-1].upper()
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
