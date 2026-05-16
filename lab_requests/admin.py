from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Request

@admin.register(Request)
class RequestAdmin(ModelAdmin):
    pass
