import json
from django.contrib.auth.models import User

from django.db import models


class Request(models.Model):

    class RequestType(models.TextChoices):
        CONTRACT = "contract", "Contract"
        SLIP = "slip", "Slip"

    class Status(models.TextChoices):
        REVIEWING = "reviewing", "Đang xem xét"
        IN_PROGRESS = "in_progress", "Đang thực hiện"
        COMPLETED = "completed", "Hoàn tất"
        CANCELLED = "cancelled", "Hủy bỏ"

    # Identity
    title = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=RequestType.choices,
        default=RequestType.SLIP,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REVIEWING,
    )

    # Relations
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="requests",
    )

    # Content
    content = models.TextField()
    participants = models.JSONField(default=list, blank=True)
    project_information = models.JSONField(default=dict, blank=True)
    requesting_unit = models.JSONField(default=dict, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def participants_json(self):
        return json.dumps(self.participants)

    @property
    def project_json(self):
        return json.dumps(self.project_information)

    @property
    def unit_json(self):
        return json.dumps(self.requesting_unit)

    def __str__(self):
        return self.title