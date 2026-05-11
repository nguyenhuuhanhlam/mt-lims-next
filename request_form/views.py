from django.contrib.auth.decorators import login_required
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