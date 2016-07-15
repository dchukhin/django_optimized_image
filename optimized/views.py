from django.shortcuts import render

from . import models


def index(request):
    return render(request, 'optimized/index.html', {'the_models': models.BlogPostOrSomething.objects.all()})
