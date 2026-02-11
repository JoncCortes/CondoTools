from django.db import models

from apps.common.models import CondoScopedModel


class Unit(CondoScopedModel):
    code = models.CharField(max_length=20)
    block = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.id)
