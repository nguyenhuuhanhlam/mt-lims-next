from django.contrib import admin

from .models import Request, MaterialTest


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass


@admin.register(MaterialTest)
class MaterialTestAdmin(admin.ModelAdmin):
    list_display = ('test_code', 'request', 'material_type', 'is_completed')
    list_filter = ('material_type',)
    search_fields = ('test_code', 'content', 'request__title')