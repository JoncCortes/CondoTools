from django.db import models

from apps.common.models import CondoScopedModel, TimeStampedModel


class ServiceProvider(CondoScopedModel):
    provider_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    document = models.CharField(max_length=80, blank=True)
    service_type = models.CharField(max_length=120)
    unit = models.ForeignKey("units.Unit", on_delete=models.SET_NULL, null=True, blank=True)
    authorized_by = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, default="ACTIVE")


class ServiceProviderAuditLog(CondoScopedModel, TimeStampedModel):
    STATUS_CHOICES = (("ACTIVE", "Active"), ("FINISHED", "Finished"), ("DENIED", "Denied"))

    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    provider_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    document = models.CharField(max_length=80, blank=True)
    service_type = models.CharField(max_length=120)
    unit = models.ForeignKey("units.Unit", on_delete=models.SET_NULL, null=True, blank=True)
    entry_at = models.DateTimeField(null=True, blank=True)
    exit_at = models.DateTimeField(null=True, blank=True)
    authorized_by = models.CharField(max_length=255, blank=True)
    registered_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="provider_registered_logs")
    finalized_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="provider_finalized_logs")
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="ACTIVE")
