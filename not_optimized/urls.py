from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^not_optimized$', views.index, name='not_optimized_index'),
]
