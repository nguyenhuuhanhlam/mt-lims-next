from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from .forms import UserForm, GroupForm

@login_required
def user_list(request):
    users = User.objects.all().order_by("-date_joined")
    
    # HTMX Searching
    q = request.GET.get('q', '').strip()
    if q:
        users = users.filter(
            models.Q(username__icontains=q) |
            models.Q(first_name__icontains=q) |
            models.Q(last_name__icontains=q) |
            models.Q(email__icontains=q)
        )
        
    if request.headers.get('HX-Request'):
        return render(request, "system_admin/partials/user_table_rows.html", {"users": users})
        
    return render(request, "system_admin/user_list.html", {"users": users, "q": q})


@login_required
def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserForm()
    return render(request, "system_admin/user_form.html", {"form": form})


@login_required
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserForm(instance=user_obj)
    return render(request, "system_admin/user_form.html", {"form": form, "is_edit": True, "user_obj": user_obj})


@login_required
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        confirm_username = request.POST.get("confirm_username", "").strip()
        if confirm_username == user_obj.username:
            user_obj.delete()
            return redirect("user_list")
        return render(request, "system_admin/user_confirm_delete.html", {
            "user_obj": user_obj,
            "error": "Tên đăng nhập không khớp. Vui lòng thử lại.",
        })
    return render(request, "system_admin/user_confirm_delete.html", {"user_obj": user_obj})


@login_required
def group_list(request):
    groups = Group.objects.all().order_by("name")
    
    # HTMX Searching
    q = request.GET.get('q', '').strip()
    if q:
        groups = groups.filter(name__icontains=q)
        
    if request.headers.get('HX-Request'):
        return render(request, "system_admin/partials/group_table_rows.html", {"groups": groups})
        
    return render(request, "system_admin/group_list.html", {"groups": groups, "q": q})


@login_required
def group_create(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("group_list")
    else:
        form = GroupForm()
    return render(request, "system_admin/group_form.html", {"form": form})


@login_required
def group_edit(request, pk):
    group_obj = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group_obj)
        if form.is_valid():
            form.save()
            return redirect("group_list")
    else:
        form = GroupForm(instance=group_obj)
    return render(request, "system_admin/group_form.html", {"form": form, "is_edit": True, "group_obj": group_obj})


@login_required
def group_delete(request, pk):
    group_obj = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        confirm_name = request.POST.get("confirm_name", "").strip()
        if confirm_name == group_obj.name:
            group_obj.delete()
            return redirect("group_list")
        return render(request, "system_admin/group_confirm_delete.html", {
            "group_obj": group_obj,
            "error": "Tên nhóm không khớp. Vui lòng thử lại.",
        })
    return render(request, "system_admin/group_confirm_delete.html", {"group_obj": group_obj})

@login_required
def group_members(request, pk):
    group_obj = get_object_or_404(Group, pk=pk)
    members = group_obj.user_set.all().order_by('username')
    return render(request, "system_admin/partials/group_members.html", {"members": members})
