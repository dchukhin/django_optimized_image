from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^optimized$', views.index, name='optimized_index'),
]
