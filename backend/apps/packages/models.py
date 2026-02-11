from django.db import models

from apps.common.models import CondoScopedModel


class Package(CondoScopedModel):
    DELIVERY_TYPES = (
        ("LETTER", "Carta registrada"),
        ("PACKAGE", "Encomenda"),
    )

    description = models.CharField(max_length=255)
    unit = models.ForeignKey("units.Unit", on_delete=models.CASCADE, related_name="packages")
    resident = models.ForeignKey("residents.Resident", on_delete=models.SET_NULL, null=True, blank=True, related_name="packages")
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPES, default="PACKAGE")
    store = models.CharField(max_length=80, blank=True)
    bank = models.CharField(max_length=80, blank=True)
    other_store = models.CharField(max_length=120, blank=True)
    other_bank = models.CharField(max_length=120, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
