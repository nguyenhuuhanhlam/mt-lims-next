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


class MaterialTest(models.Model):
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name="tests",
    )
    test_code = models.CharField(max_length=100)
    content = models.TextField()
    material_type = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    
    test_date = models.DateField(null=True, blank=True)
    result_date = models.DateField(null=True, blank=True)

    method_file = models.FileField(upload_to="tests/methods/", null=True, blank=True)
    method_uploader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_methods",
    )

    result_file = models.FileField(upload_to="tests/results/", null=True, blank=True)
    result_uploader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_results",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_completed(self):
        return bool(self.method_file and self.result_file)

    def __str__(self):
        return f"{self.test_code} - {self.material_type}"