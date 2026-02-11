from django.db import models

from apps.common.models import CondoScopedModel


class Staff(CondoScopedModel):
    full_name = models.CharField(max_length=255)
    role_name = models.CharField(max_length=80)
    user = models.OneToOneField("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
