from django.http import JsonResponse
from .models import Request


def request_list(request):

    data = list(
        Request.objects.values(
            "id",
            "title",
            "content",
            "created_at",
        )
    )

    return JsonResponse(data, safe=False)