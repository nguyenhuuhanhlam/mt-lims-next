from django.urls import path
from .views import (
    user_list, user_create, user_edit, user_delete,
    group_list, group_create, group_edit, group_delete, group_members
)

urlpatterns = [
    path("users/", user_list, name="user_list"),
    path("users/create/", user_create, name="user_create"),
    path("users/<int:pk>/edit/", user_edit, name="user_edit"),
    path("users/<int:pk>/delete/", user_delete, name="user_delete"),
    
    path("groups/", group_list, name="group_list"),
    path("groups/create/", group_create, name="group_create"),
    path("groups/<int:pk>/edit/", group_edit, name="group_edit"),
    path("groups/<int:pk>/delete/", group_delete, name="group_delete"),
    path("groups/<int:pk>/members/", group_members, name="group_members"),
]
