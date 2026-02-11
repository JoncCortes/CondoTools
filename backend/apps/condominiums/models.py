from django.db import models

from apps.common.models import TimeStampedModel


class Condominium(TimeStampedModel):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
