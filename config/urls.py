from django.contrib import admin
from django.urls import path, include

from request_form.views import (
    request_list, request_create, request_edit, request_delete, 
    request_list_api, dashboard
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),

    # Dashboard
    path("", dashboard, name="dashboard"),

    # Template views
    path("requests/", request_list, name="request_list"),
    path("requests/create/", request_create, name="request_create"),
    path("requests/<int:pk>/edit/", request_edit, name="request_edit"),
    path("requests/<int:pk>/delete/", request_delete, name="request_delete"),

    # API (legacy)
    path("api/requests/", request_list_api, name="request_list_api"),
]
