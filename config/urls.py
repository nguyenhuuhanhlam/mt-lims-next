from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from request_form.views import (
    request_list, request_create, request_edit, request_delete, 
    request_list_api, dashboard,
    test_list_partial, test_create, test_upload_file,
    test_delete, test_edit, test_cancel_edit
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

    # Material Tests (HTMX)
    path("requests/<int:request_id>/tests/", test_list_partial, name="test_list_partial"),
    path("requests/<int:request_id>/tests/create/", test_create, name="test_create"),
    path("tests/<int:test_id>/upload/<str:file_type>/", test_upload_file, name="test_upload_file"),
    path("tests/<int:test_id>/delete/", test_delete, name="test_delete"),
    path("tests/<int:test_id>/edit/", test_edit, name="test_edit"),
    path("tests/<int:test_id>/cancel_edit/", test_cancel_edit, name="test_cancel_edit"),

    # API (legacy)
    path("api/requests/", request_list_api, name="request_list_api"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
