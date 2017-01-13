from unittest.mock import patch, Mock

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from not_optimized.models import GenericModel
from optimized_image.tests.factories import OptimizedNotOptimizedFactory, GenericModelFactory
from optimized_image.utils import get_optimized_url


class TestGetOptimizedUrl(TestCase):
    """Get the optimized urls of a model instance and a field name."""
    @patch('optimized_image.fields.save_to_s3')
    def setUp(self, mock_save_to_s3):
        tinify_return_object = Mock()
        tinify_return_object.location = 'https://s3.amazonaws.com/testutils/optimized_images/image.png'
        mock_save_to_s3.return_value = tinify_return_object

        self.blog = GenericModelFactory()
        self.OptimizedNotOptimizedFactory = OptimizedNotOptimizedFactory(
            instance_model = self.blog._meta.label,
            instance_pk = self.blog.pk,
            field_name = 'image',
            url = 'image.png',
            optimized_url = 'https://s3.amazonaws.com/testutils/optimized_images/image.png'
        )

    @patch('optimized_image.fields.save_to_s3')
    def test_errors(self, mock_save_to_s3):
        """Calling get_optimized_url() with incorrect params raises an error."""
        tinify_return_object = Mock()
        tinify_return_object.location = 'https://s3.amazonaws.com/testutils/optimized_images/image.png'
        mock_save_to_s3.return_value = tinify_return_object
        # Calling get_optimized_url() with no params
        with self.assertRaises(TypeError):
            get_optimized_url()

        # Calling get_optimized_url() with incorrect field name
        with self.subTest():
            with self.assertRaises(AttributeError):
                get_optimized_url(self.blog, 'incorrectfieldname')

    @patch('optimized_image.fields.save_to_s3')
    def test_get_correct_url(self, mock_save_to_s3):
        """Calling get_optimized_url() for instance with correct field name."""
        tinify_return_object = Mock()
        tinify_return_object.location = 'https://s3.amazonaws.com/testutils/optimized_images/image.png'
        mock_save_to_s3.return_value = tinify_return_object
        result_url = get_optimized_url(self.blog, 'image')
        self.assertEqual(result_url, self.OptimizedNotOptimizedFactory.optimized_url)
