from django.contrib import admin

from . import models


@admin.register(models.Schema)
class SchemaModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Schema._meta.fields]


@admin.register(models.SchemaColumn)
class SchemaColumnModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.SchemaColumn._meta.fields]


@admin.register(models.Dataset)
class DatasetModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Dataset._meta.fields]
