from django.db import models

from apps.common.models import CondoScopedModel, TimeStampedModel


class Package(CondoScopedModel):
    DELIVERY_TYPES = (
        ("LETTER", "Carta registrada"),
        ("PACKAGE", "Encomenda"),
    )
    STATUS_CHOICES = (
        ("PENDING", "Pendente"),
        ("DELIVERED", "Entregue"),
        ("ARCHIVED", "Arquivada"),
        ("CANCELLED", "Cancelada"),
    )

    description = models.CharField(max_length=255)
    unit = models.ForeignKey("units.Unit", on_delete=models.CASCADE, related_name="packages")
    resident = models.ForeignKey("residents.Resident", on_delete=models.SET_NULL, null=True, blank=True, related_name="packages")
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPES, default="PACKAGE")
    store = models.CharField(max_length=80, blank=True)
    bank = models.CharField(max_length=80, blank=True)
    other_store = models.CharField(max_length=120, blank=True)
    other_bank = models.CharField(max_length=120, blank=True)
    tracking_code = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    received_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class PackageAuditLog(CondoScopedModel, TimeStampedModel):
    ACTIONS = (
        ("PICKED_UP", "Retirada"),
        ("RETURNED", "Retornada"),
        ("CANCELLED", "Cancelada"),
    )

    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="audit_logs")
    unit = models.ForeignKey("units.Unit", on_delete=models.SET_NULL, null=True, blank=True)
    recipient_name = models.CharField(max_length=255, blank=True)
    delivery_type = models.CharField(max_length=20, blank=True)
    store = models.CharField(max_length=80, blank=True)
    bank = models.CharField(max_length=80, blank=True)
    tracking_code = models.CharField(max_length=80, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    received_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="received_package_logs")
    picked_up_at = models.DateTimeField(null=True, blank=True)
    picked_up_by_user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="picked_package_logs")
    picked_up_by_name = models.CharField(max_length=255)
    picked_up_by_document = models.CharField(max_length=80, blank=True)
    picked_up_quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    action = models.CharField(max_length=20, choices=ACTIONS, default="PICKED_UP")
