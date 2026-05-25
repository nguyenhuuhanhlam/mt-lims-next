from django.urls import path
from .views import (
    material_test_list, user_tasks,
    test_list_partial, test_create, test_upload_file,
    test_delete, test_edit, test_cancel_edit,
    test_row_edit, test_row_cancel_edit, test_row_upload_file,
)

urlpatterns = [
    path("tests/", material_test_list, name="material_test_list"),
    path("tasks/", user_tasks, name="user_tasks"),
    path("requests/<int:request_id>/tests/", test_list_partial, name="test_list_partial"),
    path("requests/<int:request_id>/tests/create/", test_create, name="test_create"),
    path("tests/<int:test_id>/upload/<str:file_type>/", test_upload_file, name="test_upload_file"),
    path("tests/<int:test_id>/delete/", test_delete, name="test_delete"),
    path("tests/<int:test_id>/edit/", test_edit, name="test_edit"),
    path("tests/<int:test_id>/cancel_edit/", test_cancel_edit, name="test_cancel_edit"),
    path("tests/<int:test_id>/row-edit/", test_row_edit, name="test_row_edit"),
    path("tests/<int:test_id>/row-cancel/", test_row_cancel_edit, name="test_row_cancel_edit"),
    path("tests/<int:test_id>/row-upload/<str:file_type>/", test_row_upload_file, name="test_row_upload_file"),
]
