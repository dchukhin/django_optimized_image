from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^optimized$', views.index, name='optimized_index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
