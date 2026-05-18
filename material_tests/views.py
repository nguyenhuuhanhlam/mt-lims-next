from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from lab_requests.models import Request
from .models import MaterialTest
from .forms import MaterialTestForm

def not_technician(user):
    """Cho phép truy cập nếu user là superuser, Manager, hoặc không phải Technician."""
    if user.is_superuser or user.groups.filter(name="Managers").exists():
        return True
    return not user.groups.filter(name="Technicians").exists()

@login_required
def material_test_list(request):
    tests = MaterialTest.objects.select_related("request", "method_uploader", "result_uploader").order_by("-created_at")

    q = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "all")

    if q:
        tests = tests.filter(
            models.Q(test_code__icontains=q) |
            models.Q(material_type__icontains=q) |
            models.Q(request__title__icontains=q)
        )

    if status_filter == "completed":
        tests = tests.filter(status="completed")
    elif status_filter == "pending":
        tests = tests.exclude(status="completed")

    filter_options = [
        ("all", "Tất cả"),
        ("completed", "Hoàn tất"),
        ("pending", "Chờ file"),
    ]

    if request.headers.get("HX-Request"):
        return render(request, "material_tests/partials/material_test_table_rows.html", {"tests": tests, "q": q, "status_filter": status_filter})

    return render(request, "material_tests/material_test_list.html", {"tests": tests, "q": q, "status_filter": status_filter, "filter_options": filter_options})


@login_required
def test_list_partial(request, request_id):
    req_obj = get_object_or_404(Request, pk=request_id)
    tests = req_obj.tests.all().order_by('-created_at')
    form = MaterialTestForm(user=request.user)
    return render(request, "material_tests/partials/test_list.html", {
        "request_obj": req_obj,
        "tests": tests,
        "form": form
    })


@login_required
@user_passes_test(not_technician)
def test_create(request, request_id):
    req_obj = get_object_or_404(Request, pk=request_id)
    if request.method == "POST":
        form = MaterialTestForm(request.POST, user=request.user)
        if form.is_valid():
            test = form.save(commit=False)
            test.request = req_obj
            test.save()
            tests = req_obj.tests.all().order_by('-created_at')
            return render(request, "material_tests/partials/test_list.html", {
                "request_obj": req_obj,
                "tests": tests,
                "form": MaterialTestForm(user=request.user)
            })
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def test_upload_file(request, test_id, file_type):
    test = get_object_or_404(MaterialTest, pk=test_id)
    if request.method == "POST":
        file_obj = request.FILES.get('file')
        if file_obj:
            if file_type == 'method':
                test.method_file = file_obj
                test.method_uploader = request.user
            elif file_type == 'result':
                test.result_file = file_obj
                test.result_uploader = request.user
            test.save()
            return render(request, "material_tests/partials/test_card.html", {"test": test})
    return JsonResponse({"error": "Upload failed"}, status=400)


@login_required
@user_passes_test(not_technician)
def test_delete(request, test_id):
    test = get_object_or_404(MaterialTest, pk=test_id)
    if request.method == "DELETE":
        test.delete()
        return HttpResponse("")
    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
@user_passes_test(not_technician)
def test_edit(request, test_id):
    test = get_object_or_404(MaterialTest, pk=test_id)
    if request.method == "POST":
        form = MaterialTestForm(request.POST, instance=test, user=request.user)
        if form.is_valid():
            form.save()
            return render(request, "material_tests/partials/test_card.html", {"test": test})
    else:
        form = MaterialTestForm(instance=test, user=request.user)
    return render(request, "material_tests/partials/test_edit_card.html", {"test": test, "form": form})


@login_required
def test_cancel_edit(request, test_id):
    test = get_object_or_404(MaterialTest, pk=test_id)
    return render(request, "material_tests/partials/test_card.html", {"test": test})


@login_required
def test_row_edit(request, test_id):
    """Trả về edit row (form nằm trong <tr>) để inline edit trên trang danh sách."""
    test = get_object_or_404(MaterialTest, pk=test_id)
    is_tech = not not_technician(request.user)
    if request.method == "POST":
        # Technician không được lưu (nút Lưu bị ẩn trong template, nhưng bảo vệ thêm ở backend)
        if is_tech:
            return HttpResponse(status=403)
        form = MaterialTestForm(request.POST, instance=test, user=request.user)
        if form.is_valid():
            form.save()
            return render(request, "material_tests/partials/material_test_row.html", {"test": test})
    else:
        form = MaterialTestForm(instance=test, user=request.user)
    return render(request, "material_tests/partials/material_test_edit_row.html", {"test": test, "form": form})


@login_required
def test_row_cancel_edit(request, test_id):
    """Hủy inline edit — trả về display row bình thường."""
    test = get_object_or_404(MaterialTest, pk=test_id)
    return render(request, "material_tests/partials/material_test_row.html", {"test": test})


@login_required
def test_row_upload_file(request, test_id, file_type):
    """Upload file (method/result) từ trang danh sách /tests — render lại material_test_row."""
    test = get_object_or_404(MaterialTest, pk=test_id)
    if request.method == "POST":
        file_obj = request.FILES.get("file")
        if file_obj:
            if file_type == "method":
                test.method_file = file_obj
                test.method_uploader = request.user
            elif file_type == "result":
                test.result_file = file_obj
                test.result_uploader = request.user
            test.save()
            return render(request, "material_tests/partials/material_test_row.html", {"test": test})
    return JsonResponse({"error": "Upload failed"}, status=400)
