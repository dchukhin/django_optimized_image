from factory.fuzzy import FuzzyText
import io
from unittest.mock import patch, Mock

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from . import factories
from ..utils import optimize_from_buffer, optimize_legacy_images_in_model_fields


class TestOptimizeFromBuffer(TestCase):
    """Test case for the mock_optimize_from_buffer() function."""
    @patch('optimized_image.utils.is_testing_mode')
    @patch('optimized_image.utils.Image')
    @patch('optimized_image.utils.tinify')
    def test_settings(self, mock_tinify, mock_pil_image, mock_is_testing_mode):
        """
        Calling optimize_from_buffer() only optimizes images if not in testing mode.

        Moreover, the OPTIMIZED_IMAGE_METHOD determines whether Pillow or TinyPNG
        are used for the optimization.
        """
        mock_obj = Mock()
        mock_obj.name = 'test_image.png'

        ignore_obj = Mock()
        ignore_obj.name = 'ignore_image.gif'

        testing_mode_subtests = (
            # testing_mode, optimized_image_method
            (True, 'pillow'),
            (True, 'tinypng'),
            (True, 'other'),
        )
        non_testing_mode_subtests = (
            # testing_mode, optimized_image_method
            (False, 'pillow'),
            (False, 'tinypng'),
            (False, 'other'),
        )
        for testing_mode, optimized_image_method in testing_mode_subtests:
            mock_is_testing_mode.return_value = testing_mode

            with self.subTest(testing_mode=testing_mode, optimized_image_method=optimized_image_method):
                with self.settings(
                    OPTIMIZED_IMAGE_METHOD=optimized_image_method,
                    OPTIMIZED_IMAGE_IGNORE_EXTENSIONS=['gif'],
                ):
                    optimize_from_buffer(mock_obj)
                    optimize_from_buffer(ignore_obj)
                    self.assertFalse(mock_tinify.called)

        for testing_mode, optimized_image_method in non_testing_mode_subtests:
            with self.subTest(testing_mode=testing_mode, optimized_image_method=optimized_image_method):
                with self.settings(
                    OPTIMIZED_IMAGE_METHOD=optimized_image_method,
                    OPTIMIZED_IMAGE_IGNORE_EXTENSIONS=['gif'],
                ):
                    mock_is_testing_mode.return_value = testing_mode

                    start_pil_image_call_count = mock_pil_image.open.call_count
                    start_tinify_from_buffer_call_count = mock_tinify.from_buffer.call_count

                    optimize_from_buffer(mock_obj)
                    optimize_from_buffer(ignore_obj)

                    if optimized_image_method == 'pillow':
                        expected_pil_calls = start_pil_image_call_count + 1
                    else:
                        expected_pil_calls = start_pil_image_call_count
                    if optimized_image_method == 'tinypng':
                        expected_tinify_calls = start_tinify_from_buffer_call_count + 1
                    else:
                        expected_tinify_calls = start_tinify_from_buffer_call_count

                    # Assert the expected number of calls
                    self.assertEqual(mock_pil_image.open.call_count, expected_pil_calls)
                    self.assertEqual(mock_tinify.from_buffer.call_count, expected_tinify_calls)


class TestOptimizeLegacyImagesInModelFields(TestCase):
    @patch('optimized_image.utils.Image')
    @patch('optimized_image.utils.tinify')
    def test_settings(self, mock_tinify, mock_pil_image):
        """The OPTIMIZED_IMAGE_METHOD is used to determine whether Pillow or TinyPNG is used."""
        generic_model = factories.GenericModelFactory()

        with self.subTest(OPTIMIZED_IMAGE_METHOD='pillow'):
            with self.settings(
                OPTIMIZED_IMAGE_METHOD='pillow',
                OPTIMIZED_IMAGE_IGNORE_EXTENSIONS=['gif'],
            ):
                # So far neither Pillow nor TinyPNG have been called
                self.assertFalse(mock_pil_image.open.called)
                self.assertFalse(mock_tinify.from_buffer.called)

                optimize_legacy_images_in_model_fields([generic_model.__class__])

                # Now the Pillow method has been called once
                self.assertEqual(mock_pil_image.open.call_count, 1)
                self.assertFalse(mock_tinify.from_buffer.called)

        with self.subTest(OPTIMIZED_IMAGE_METHOD='tinypng'):
            with self.settings(
                OPTIMIZED_IMAGE_METHOD='tinypng',
                OPTIMIZED_IMAGE_IGNORE_EXTENSIONS=['gif'],
            ):
                # So far Pillow has been called once (in the other subTest), but
                # TinyPNG has not been called.
                self.assertEqual(mock_pil_image.open.call_count, 1)
                self.assertFalse(mock_tinify.from_buffer.called)

                optimize_legacy_images_in_model_fields([generic_model.__class__])

                # Now the Pillow and TinyPNG methods have each been called once.
                self.assertEqual(mock_pil_image.open.call_count, 1)
                self.assertTrue(mock_tinify.from_buffer.call_count, 1)

    @patch('optimized_image.utils.Image')
    def test_class_optimizes_all_instances(self, mock_pil_image):
        """Calling the funciton with a class optimizes all images for all instance of that class."""
        # We use the Pillow optimization for this test
        with self.settings(
            OPTIMIZED_IMAGE_METHOD='pillow',
            OPTIMIZED_IMAGE_IGNORE_EXTENSIONS=['gif'],
        ):
            # Several models that have several image fields each, with images
            blog1 = factories.BlogPostOrSomethingFactory(title='Blog 1')
            blog2 = factories.BlogPostOrSomethingFactory(title='Blog 2')
            for blogpost in [blog1, blog2]:
                self.assertNotEqual(blogpost.image1.name, '')
                self.assertNotEqual(blogpost.image2.name, '')
            # So far the Pillow method has not been called
            self.assertFalse(mock_pil_image.open.called)

            # Call optimize_legacy_images_in_model_fields(), passing in the class of
            # the blog objects
            optimize_legacy_images_in_model_fields([blog1.__class__])

            # The image1 and image2 fields for both blog posts should have been optimized
            images = [blog1.image1, blog1.image2, blog2.image1, blog2.image2]
            # These are the expected inputs into PIL.Image.open()
            expected_pil_image_open_calls = [
                io.BytesIO(image.read()).getvalue() for image in images
            ]
            self.assertEqual(mock_pil_image.open.call_count, len(images))
            pil_image_open_calls = [
                call[0][0].getvalue() for call in mock_pil_image.open.call_args_list
            ]
            self.assertEqual(expected_pil_image_open_calls, pil_image_open_calls)
