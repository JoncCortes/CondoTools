from django.db import models

from apps.common.models import CondoScopedModel


class CommonArea(CondoScopedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)
