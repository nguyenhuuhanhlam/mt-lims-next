from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import RequestForm
from .models import Request

def not_technician(user):
    """Cho phép truy cập nếu user là superuser, Manager, hoặc không phải Technician."""
    if user.is_superuser or user.groups.filter(name="Managers").exists():
        return True
    return not user.groups.filter(name="Technicians").exists()

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
        return render(request, "lab_requests/partials/request_table_rows.html", {"requests": requests})
        
    return render(request, "lab_requests/request_list.html", {"requests": requests})


@login_required
@user_passes_test(not_technician)
def request_create(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("request_list")
    else:
        form = RequestForm(initial={"created_by": request.user})
    return render(request, "lab_requests/request_create.html", {"form": form})


@login_required
@user_passes_test(not_technician)
def request_edit(request, pk):
    instance = Request.objects.get(pk=pk)
    if request.method == "POST":
        form = RequestForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("request_list")
    else:
        form = RequestForm(instance=instance)
    return render(request, "lab_requests/request_create.html", {"form": form, "is_edit": True})


@login_required
@user_passes_test(not_technician)
def request_delete(request, pk):
    instance = Request.objects.get(pk=pk)
    if request.method == "POST":
        confirm_title = request.POST.get("confirm_title", "").strip()
        if confirm_title == instance.title:
            instance.delete()
            return redirect("request_list")
        return render(request, "lab_requests/request_confirm_delete.html", {
            "request_obj": instance,
            "error": "Tên phiếu không khớp. Vui lòng thử lại.",
        })
    return render(request, "lab_requests/request_confirm_delete.html", {"request_obj": instance})


def request_list_api(request):
    data = list(
        Request.objects.values(
            "id", "title", "type", "content", "created_at",
        )
    )
    return JsonResponse(data, safe=False)