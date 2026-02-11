from django.db import models

from apps.common.models import CondoScopedModel


class Incident(CondoScopedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=32, default="OPEN")
    reporter = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
