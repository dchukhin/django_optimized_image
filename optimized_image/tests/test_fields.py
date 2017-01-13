from unittest.mock import patch, Mock

from django.test import TestCase

from . import factories


class TestOptimizedImageField(TestCase):
    """Test case for the OptimizedImageField."""

    @patch('optimized_image.fields.save_to_s3')
    def test_save_creates_optimized_image(self, mock_save_to_s3):
        """Saving an image to an OptimizedImageField creates optimized image."""
        tinify_return_object = Mock()
        tinify_return_object.location = 'https://s3.amazonaws.com/testutils/optimized_images/image.png'
        mock_save_to_s3.return_value = tinify_return_object

        # import ipdb; ipdb.set_trace()
        generic_model = factories.GenericModelFactory(
            title='Generic Model',
            image=None
        )
        from optimized_image.models import OptimizedNotOptimized

        # So far there is no optimized image, and mock_save_to_s3 has not been called
        self.assertEqual(generic_model.image.name, None)
        self.assertEqual(generic_model.image.optimized_url, '')
        self.assertEqual(mock_save_to_s3.call_count, 0)

        import io
        new_io = io.StringIO()
        new_io.write('something')
        from django.core.files.uploadedfile import InMemoryUploadedFile
        new_file=InMemoryUploadedFile(new_io, 'image', 'static/images/vvv.png', 'image/jpeg', len(new_io.getvalue()), 'utf-8')
        generic_model.image = new_file
        generic_model.save()

        # Now generic_model.image has an optimized_url
        self.assertNotEqual(generic_model.image.name, None)
        self.assertEqual(generic_model.image.optimized_url, mock_save_to_s3.return_value.location)
        # The mock_save_to_s3 has been called once
        self.assertEqual(mock_save_to_s3.call_count, 1)

    # TODO: also test the OptimizedImageFieldFile things:
    #   - optimized_url field
    #   - delete() deletes the OptimizedNotOptimized object
