from django.db import models

from apps.common.models import CondoScopedModel


class Reservation(CondoScopedModel):
    common_area = models.ForeignKey("common_areas.CommonArea", on_delete=models.CASCADE, related_name="reservations")
    unit = models.ForeignKey("units.Unit", on_delete=models.CASCADE, related_name="reservations")
    resident = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=32, default="REQUESTED")

    def __str__(self):
        return str(self.id)
