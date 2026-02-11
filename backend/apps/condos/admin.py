from django.contrib import admin

from . import models

for model in [
    models.Condominium,
    models.Unit,
    models.Resident,
    models.Staff,
    models.Visitor,
    models.VisitLog,
    models.Package,
    models.Announcement,
    models.Incident,
    models.CommonArea,
    models.Reservation,
]:
    admin.site.register(model)
