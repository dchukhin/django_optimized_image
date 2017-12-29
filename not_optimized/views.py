from django.shortcuts import render

from .models import BlogPostOrSomething


def index(request):
    return render(
        request,
        'optimized/index.html',
        {'the_models': BlogPostOrSomething.objects.all(),
        }
    )
