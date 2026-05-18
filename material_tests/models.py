import os
from django.contrib.auth.models import User
from django.db import models
from lab_requests.models import Request

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

    status = models.CharField(
        max_length=20,
        choices=[("in_progress", "Đang thực hiện"), ("completed", "Hoàn tất")],
        default="in_progress",
    )
    tester = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tests",
        limit_choices_to={'groups__name': 'Technicians'},
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_tests",
        limit_choices_to={'groups__name': 'Managers'},
    )

    @property
    def is_completed(self):
        return self.status == "completed"

    def delete(self, *args, **kwargs):
        # Xóa file vật lý khỏi disk trước khi xóa record
        if self.method_file:
            if os.path.isfile(self.method_file.path):
                os.remove(self.method_file.path)
        if self.result_file:
            if os.path.isfile(self.result_file.path):
                os.remove(self.result_file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.test_code} - {self.material_type}"
