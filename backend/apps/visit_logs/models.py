from django.db import models

from apps.common.models import CondoScopedModel


class VisitLog(CondoScopedModel):
    visitor = models.ForeignKey("visitors.Visitor", on_delete=models.CASCADE, related_name="visit_logs")
    entry_at = models.DateTimeField()
    exit_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)
