#!/usr/bin/env python
import sys
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "test.db",}
        },
        MIDDLEWARE_CLASSES=(),
        INSTALLED_APPS=("optimized_image", "not_optimized"),
        SITE_ID=1,
        ADMINS=(("Admin", "admin@example.com"),),
        OPTIMIZED_IMAGE_METHOD="pillow",
        TINYPNG_KEY="versecrettinypngkey",
        BASE_DIR="",  # tells compatibility checker not to emit warning
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": ["optimized_image/templates"],
            }
        ],
    )


def runtests():
    django.setup()
    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=True)
    failures = test_runner.run_tests(["optimized_image"])
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    runtests()
