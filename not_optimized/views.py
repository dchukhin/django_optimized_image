from django.shortcuts import render

from optimized_image.models import OptimizedNotOptimized

from .models import BlogPostOrSomething


def index(request):
    return render(
        request,
        'optimized/index.html',
        {'the_models': BlogPostOrSomething.objects.all(),
         'image_urls': OptimizedNotOptimized.objects.all()
        }
    )
