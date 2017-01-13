from django.test import TestCase

from . import factories


class TestOptimizedNotOptimized(TestCase):
    """Test for the OptimizedNotOptimized model."""

    def test_str(self):
        """Smoke test for string representation."""
        ono = factories.OptimizedNotOptimizedFactory(
            instance_model='NewModel',
            instance_pk=1,
            field_name='image_field'
        )
        self.assertEqual(str(ono), "{} pk {} optimized field {}".format(
            ono.instance_model,
            ono.instance_pk,
            ono.field_name)
        )
