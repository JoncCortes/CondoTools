from django.db import models

from apps.accounts.models import User


class RolePermissionSet(models.Model):
    role = models.CharField(max_length=20, choices=User.Role.choices)
    condominium = models.ForeignKey("condominiums.Condominium", null=True, blank=True, on_delete=models.CASCADE)
    permissions = models.JSONField(default=list, blank=True)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_role_permissions")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("role", "condominium")
        ordering = ["role", "id"]
