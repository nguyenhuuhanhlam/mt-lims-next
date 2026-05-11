from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import RequestForm
from .models import Request


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
        instance.delete()
        return redirect("request_list")
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