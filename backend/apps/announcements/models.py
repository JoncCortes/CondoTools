from django.db import models

from apps.common.models import CondoScopedModel


class Announcement(CondoScopedModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return str(self.id)
