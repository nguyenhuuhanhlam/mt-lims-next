from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import RequestForm, MaterialTestForm
from .models import Request, MaterialTest


# ─── API (giữ lại để tương thích) ──────────────────────────
def request_list_api(request):
    data = list(
        Request.objects.values(
            "id", "title", "type", "content", "created_at",
        )
    )
    return JsonResponse(data, safe=False)


# ─── Template Views ─────────────────────────────────────────
@login_required
def request_list(request):
    requests = Request.objects.select_related("created_by").order_by("-created_at")
    
    # HTMX Filtering
    query = request.GET.get('q', '')
    req_type = request.GET.get('type', 'all')
    
    if query:
        requests = requests.filter(title__icontains=query)
    
    if req_type != 'all':
        requests = requests.filter(type=req_type)
        
    if request.headers.get('HX-Request'):
        return render(request, "request_form/partials/request_table_rows.html", {"requests": requests})
        
    return render(request, "request_form/request_list.html", {"requests": requests})


@login_required
def request_create(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("request_list")
    else:
        form = RequestForm(initial={"created_by": request.user})
    return render(request, "request_form/request_create.html", {"form": form})


@login_required
def request_edit(request, pk):
    instance = Request.objects.get(pk=pk)
    if request.method == "POST":
        form = RequestForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("request_list")
    else:
        form = RequestForm(instance=instance)
    return render(request, "request_form/request_create.html", {"form": form, "is_edit": True})


@login_required
def request_delete(request, pk):
    instance = Request.objects.get(pk=pk)
    if request.method == "POST":
        confirm_title = request.POST.get("confirm_title", "").strip()
        if confirm_title == instance.title:
            instance.delete()
            return redirect("request_list")
        # Tên không khớp — render lại trang với thông báo lỗi
        return render(request, "request_form/request_confirm_delete.html", {
            "request_obj": instance,
            "error": "Tên phiếu không khớp. Vui lòng thử lại.",
        })
    return render(request, "request_form/request_confirm_delete.html", {"request_obj": instance})


@login_required
def dashboard(request):
    today = timezone.now().date()
    context = {
        "total_requests":  Request.objects.count(),
        "total_contracts": Request.objects.filter(type="contract").count(),
        "total_slips":     Request.objects.filter(type="slip").count(),
        "today_requests":  Request.objects.filter(created_at__date=today).count(),
        "recent_requests": Request.objects.order_by("-created_at")[:8],
    }
    return render(request, "dashboard.html", context)


# ─── Material Test List (trang độc lập) ────────────────────────────────

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
        tests = [t for t in tests if t.is_completed]
    elif status_filter == "pending":
        tests = [t for t in tests if not t.is_completed]

    filter_options = [
        ("all", "Tất cả"),
        ("completed", "Hoàn tất"),
        ("pending", "Chờ file"),
    ]

    if request.headers.get("HX-Request"):
        return render(request, "request_form/partials/material_test_table_rows.html", {"tests": tests, "q": q, "status_filter": status_filter})

    return render(request, "request_form/material_test_list.html", {"tests": tests, "q": q, "status_filter": status_filter, "filter_options": filter_options})


# ─── Material Test Views (HTMX) ─────────────────────────────────────────

@login_required
def test_list_partial(request, request_id):
    req_obj = get_object_or_404(Request, pk=request_id)
    tests = req_obj.tests.all().order_by('-created_at')
    form = MaterialTestForm()
    return render(request, "request_form/partials/test_list.html", {
        "request_obj": req_obj,
        "tests": tests,
        "form": form
    })


@login_required
def test_create(request, request_id):
    req_obj = get_object_or_404(Request, pk=request_id)
    if request.method == "POST":
        form = MaterialTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.request = req_obj
            test.save()
            tests = req_obj.tests.all().order_by('-created_at')
            return render(request, "request_form/partials/test_list.html", {
                "request_obj": req_obj,
                "tests": tests,
                "form": MaterialTestForm()
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
            return render(request, "request_form/partials/test_card.html", {"test": test})
    return JsonResponse({"error": "Upload failed"}, status=400)


@login_required
def test_delete(request, test_id):
    test = get_object_or_404(MaterialTest, pk=test_id)
    if request.method == "DELETE":
        test.delete()
        return HttpResponse("")
    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
def test_edit(request, test_id):
    test = get_object_or_404(MaterialTest, pk=test_id)
    if request.method == "POST":
        form = MaterialTestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return render(request, "request_form/partials/test_card.html", {"test": test})
    else:
        form = MaterialTestForm(instance=test)
    return render(request, "request_form/partials/test_edit_card.html", {"test": test, "form": form})


@login_required
def test_cancel_edit(request, test_id):
    test = get_object_or_404(MaterialTest, pk=test_id)
    return render(request, "request_form/partials/test_card.html", {"test": test})


# ─── Row Inline Edit (dùng cho trang material_test_list) ────────────────

@login_required
def test_row_edit(request, test_id):
    """Trả về edit row (form nằm trong <tr>) để inline edit trên trang danh sách."""
    test = get_object_or_404(MaterialTest, pk=test_id)
    if request.method == "POST":
        form = MaterialTestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return render(request, "request_form/partials/material_test_row.html", {"test": test})
    else:
        form = MaterialTestForm(instance=test)
    return render(request, "request_form/partials/material_test_edit_row.html", {"test": test, "form": form})


@login_required
def test_row_cancel_edit(request, test_id):
    """Hủy inline edit — trả về display row bình thường."""
    test = get_object_or_404(MaterialTest, pk=test_id)
    return render(request, "request_form/partials/material_test_row.html", {"test": test})


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
            return render(request, "request_form/partials/material_test_row.html", {"test": test})
    return JsonResponse({"error": "Upload failed"}, status=400)