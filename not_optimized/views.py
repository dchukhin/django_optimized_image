from django.shortcuts import render


def index(request):
    return render(request, 'not_optimized/index.html')
