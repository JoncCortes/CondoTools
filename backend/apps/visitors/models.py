from django.db import models

from apps.common.models import CondoScopedModel, TimeStampedModel


class Visitor(CondoScopedModel):
    full_name = models.CharField(max_length=255)
    document = models.CharField(max_length=32)
    unit = models.ForeignKey("units.Unit", on_delete=models.SET_NULL, null=True, blank=True)
    authorized_by = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class VisitorAuditLog(CondoScopedModel, TimeStampedModel):
    STATUS_CHOICES = (("INSIDE", "Inside"), ("EXITED", "Exited"), ("DENIED", "Denied"))

    visitor = models.ForeignKey(Visitor, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    visitor_name = models.CharField(max_length=255)
    document = models.CharField(max_length=32, blank=True)
    unit = models.ForeignKey("units.Unit", on_delete=models.SET_NULL, null=True, blank=True)
    authorized_by = models.CharField(max_length=255, blank=True)
    entry_at = models.DateTimeField(null=True, blank=True)
    exit_at = models.DateTimeField(null=True, blank=True)
    registered_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="visitor_registered_logs")
    finalized_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="visitor_finalized_logs")
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="INSIDE")
