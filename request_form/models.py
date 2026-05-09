from django.contrib.auth.models import User
from django.db import models


class Request(models.Model):

    class RequestType(models.TextChoices):
        CONTRACT = "contract", "Contract"
        SLIP = "slip", "Slip"

    # Identity
    title = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=RequestType.choices,
        default=RequestType.SLIP,
    )

    # Relations
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="requests",
    )

    # Content
    content = models.TextField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title