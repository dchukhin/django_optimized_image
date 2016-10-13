from django.contrib import admin

from . import models


@admin.register(models.BlogPostOrSomething)
class BlogPostOrSomethingAdmin(admin.ModelAdmin):
    pass
