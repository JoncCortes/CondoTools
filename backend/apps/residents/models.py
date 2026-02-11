from django.db import models

from apps.common.models import CondoScopedModel


class Resident(CondoScopedModel):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    unit = models.ForeignKey("units.Unit", on_delete=models.CASCADE, related_name="residents")
    user = models.OneToOneField("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    document = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    photo_url = models.URLField(blank=True)
    status = models.CharField(max_length=30, default="ACTIVE")

    def __str__(self):
        return str(self.id)
