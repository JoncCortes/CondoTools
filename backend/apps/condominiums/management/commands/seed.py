from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.condominiums.models import Condominium
from apps.residents.models import Resident
from apps.staff.models import Staff
from apps.units.models import Unit


class Command(BaseCommand):
    help = "Seed inicial"

    def handle(self, *args, **options):
        User = get_user_model()

        condo, _ = Condominium.objects.get_or_create(
            document="12.345.678/0001-90",
            defaults={"name": "Condomínio Aurora", "address": "Rua Central, 100"},
        )
        unit, _ = Unit.objects.get_or_create(condominium=condo, code="101", block="A")

        User.objects.get_or_create(
            email="admin@platform.com",
            defaults={"role": User.Role.PLATFORM_ADMIN, "is_staff": True, "is_superuser": True},
        )
        sindico, _ = User.objects.get_or_create(
            email="sindico@aurora.com", defaults={"role": User.Role.SINDICO, "condominium": condo}
        )
        sindico.set_password("123456")
        sindico.save()

        porteiro, _ = User.objects.get_or_create(
            email="porteiro@aurora.com", defaults={"role": User.Role.PORTEIRO, "condominium": condo}
        )
        porteiro.set_password("123456")
        porteiro.save()

        morador, _ = User.objects.get_or_create(
            email="morador@aurora.com", defaults={"role": User.Role.MORADOR, "condominium": condo}
        )
        morador.set_password("123456")
        morador.save()

        Staff.objects.get_or_create(condominium=condo, user=porteiro, defaults={"full_name": "Carlos", "role_name": "Porteiro"})
        Resident.objects.get_or_create(condominium=condo, user=morador, unit=unit, defaults={"full_name": "Ana"})

        self.stdout.write(self.style.SUCCESS("Seed executado com sucesso."))
