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
def request_list(request):
    requests = Request.objects.select_related("created_by").order_by("-created_at")
    return render(request, "request_form/request_list.html", {"requests": requests})


def request_create(request):
    form = RequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.created_by = request.user
        obj.save()
        return redirect("request_list")
    return render(request, "request_form/request_create.html", {"form": form})


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