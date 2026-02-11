from django.db import models

from apps.common.models import CondoScopedModel


class Package(CondoScopedModel):
    description = models.CharField(max_length=255)
    unit = models.ForeignKey("units.Unit", on_delete=models.CASCADE, related_name="packages")
    received_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
