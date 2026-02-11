from django.db import models

from apps.common.models import CondoScopedModel


class Resident(CondoScopedModel):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    unit = models.ForeignKey("units.Unit", on_delete=models.CASCADE, related_name="residents")
    user = models.OneToOneField("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
