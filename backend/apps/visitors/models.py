from django.db import models

from apps.common.models import CondoScopedModel


class Visitor(CondoScopedModel):
    full_name = models.CharField(max_length=255)
    document = models.CharField(max_length=32)
    unit = models.ForeignKey("units.Unit", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.id)
