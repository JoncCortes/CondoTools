from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.accounts.models import RoleChoices
from apps.condos.models import Condominium, Resident, Staff, Unit


class Command(BaseCommand):
    help = "Popula dados iniciais do MVP"

    def handle(self, *args, **options):
        User = get_user_model()
        condo, _ = Condominium.objects.get_or_create(
            document="12.345.678/0001-90",
            defaults={"name": "Condomínio Aurora", "address": "Rua das Flores, 100"},
        )

        unit101, _ = Unit.objects.get_or_create(condominium=condo, number="101", block="A", code="A-101")
        unit102, _ = Unit.objects.get_or_create(condominium=condo, number="102", block="A", code="A-102")

        sindico, _ = User.objects.get_or_create(
            username="sindico",
            defaults={"email": "sindico@aurora.com", "role": RoleChoices.SINDICO, "condominium": condo},
        )
        sindico.set_password("123456")
        sindico.save()

        porteiro, _ = User.objects.get_or_create(
            username="porteiro",
            defaults={"email": "porteiro@aurora.com", "role": RoleChoices.PORTEIRO, "condominium": condo},
        )
        porteiro.set_password("123456")
        porteiro.save()

        morador, _ = User.objects.get_or_create(
            username="morador",
            defaults={"email": "morador@aurora.com", "role": RoleChoices.MORADOR, "condominium": condo},
        )
        morador.set_password("123456")
        morador.save()

        Staff.objects.get_or_create(condominium=condo, user=porteiro, defaults={"full_name": "Carlos Porteiro", "role_name": "Porteiro"})
        Resident.objects.get_or_create(condominium=condo, user=morador, unit=unit101, defaults={"full_name": "Ana Moradora", "phone": "11999999999"})

        self.stdout.write(self.style.SUCCESS("Seed do MVP executada com sucesso."))
