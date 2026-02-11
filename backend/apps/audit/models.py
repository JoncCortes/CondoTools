from django.db import models

from apps.common.models import TimeStampedModel


class AuditLog(TimeStampedModel):
    ACTION_CHOICES = (("CREATE", "CREATE"), ("UPDATE", "UPDATE"), ("DELETE", "DELETE"))

    user = models.ForeignKey("accounts.User", null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=120)
    object_id = models.CharField(max_length=64)
    condominium = models.ForeignKey("condominiums.Condominium", null=True, blank=True, on_delete=models.SET_NULL)
    changes = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
