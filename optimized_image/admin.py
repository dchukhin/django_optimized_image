from django.contrib import admin

from . import models


@admin.register(models.OptimizedNotOptimized)
class OptimizedNotOptimizedAdmin(admin.ModelAdmin):
    pass
