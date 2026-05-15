from django.urls import path
from .views import (
    request_list, request_create, request_edit, request_delete,
    request_list_api,
)

urlpatterns = [
    path("requests/", request_list, name="request_list"),
    path("requests/create/", request_create, name="request_create"),
    path("requests/<int:pk>/edit/", request_edit, name="request_edit"),
    path("requests/<int:pk>/delete/", request_delete, name="request_delete"),
    path("api/requests/", request_list_api, name="request_list_api"),
]
