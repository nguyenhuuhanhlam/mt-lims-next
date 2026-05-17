from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import MaterialTest

@admin.register(MaterialTest)
class MaterialTestAdmin(ModelAdmin):
    list_display = ('test_code', 'request', 'material_type', 'is_completed')
    list_filter = ('material_type',)
    search_fields = ('test_code', 'content', 'request__title')
