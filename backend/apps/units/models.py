from django.db import models

from apps.common.models import CondoScopedModel


class Unit(CondoScopedModel):
    code = models.CharField(max_length=40, blank=True, default="")
    number = models.CharField(max_length=40)
    block = models.CharField(max_length=40, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return f"Bloco {self.block} - {self.number}" if self.block else self.number
