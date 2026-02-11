from django.db import models

from apps.common.models import CondoScopedModel, TimeStampedModel


class Condominium(TimeStampedModel):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Unit(CondoScopedModel):
    code = models.CharField(max_length=20)
    block = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = ("condominium", "code", "block")


class Resident(CondoScopedModel):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="residents")
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)


class Staff(CondoScopedModel):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    role_name = models.CharField(max_length=80)


class Visitor(CondoScopedModel):
    full_name = models.CharField(max_length=255)
    document = models.CharField(max_length=32)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)


class VisitLog(CondoScopedModel):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name="visit_logs")
    entry_at = models.DateTimeField()
    exit_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)


class Package(CondoScopedModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="packages")
    received_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    received_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)


class Announcement(CondoScopedModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)


class Incident(CondoScopedModel):
    reporter = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=40, default="OPEN")


class CommonArea(CondoScopedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class Reservation(CondoScopedModel):
    common_area = models.ForeignKey(CommonArea, on_delete=models.CASCADE, related_name="reservations")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="reservations")
    resident = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=40, default="REQUESTED")
