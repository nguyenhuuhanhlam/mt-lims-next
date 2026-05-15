from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from lab_requests.models import Request

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
    return render(request, "core/dashboard.html", context)
