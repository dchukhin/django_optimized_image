from django.contrib import admin

from . import models


@admin.register(models.BlogPostOrSomething)
class BlogPostOrSomethingAdmin(admin.ModelAdmin):
    pass

@admin.register(models.GenericModel)
class GenericModel(admin.ModelAdmin):
    pass
