from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.common_areas.models import CommonArea
from apps.condominiums.models import Condominium
from apps.packages.models import Package
from apps.residents.models import Resident
from apps.settings_menu.models import MenuCategory, MenuItem
from apps.staff.models import Staff
from apps.visitors.models import Visitor, VisitorAuditLog
from apps.service_providers.models import ServiceProvider, ServiceProviderAuditLog
from apps.units.models import Unit


class Command(BaseCommand):
    help = "Seed inicial"

    def handle(self, *args, **options):
        User = get_user_model()

        condo, _ = Condominium.objects.get_or_create(
            document="12.345.678/0001-90",
            defaults={"name": "Condomínio Aurora", "address": "Rua Central, 100"},
        )
        unit101, _ = Unit.objects.get_or_create(condominium=condo, number="101", block="A", defaults={"code": "A-101"})
        unit102, _ = Unit.objects.get_or_create(condominium=condo, number="102", block="A", defaults={"code": "A-102"})

        admin, _ = User.objects.get_or_create(
            email="admin@platform.com",
            defaults={"role": User.Role.PLATFORM_ADMIN, "is_staff": True, "is_superuser": True},
        )
        admin.set_password("123456")
        admin.save()

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
        resident1, _ = Resident.objects.get_or_create(
            condominium=condo,
            user=morador,
            unit=unit101,
            defaults={"full_name": "Ana", "phone": "11999999999"},
        )
        Resident.objects.get_or_create(
            condominium=condo,
            unit=unit102,
            defaults={"full_name": "João", "phone": "11988887777"},
        )

        CommonArea.objects.get_or_create(condominium=condo, name="Salão de festas", defaults={"description": "Espaço para eventos"})
        CommonArea.objects.get_or_create(condominium=condo, name="Churrasqueira", defaults={"description": "Área gourmet"})


        visitor, _ = Visitor.objects.get_or_create(condominium=condo, full_name="Visitante Demo", document="999999999", unit=unit101, defaults={"authorized_by":"Portaria", "is_active":True})
        VisitorAuditLog.objects.get_or_create(condominium=condo, visitor=visitor, visitor_name=visitor.full_name, document=visitor.document, unit=visitor.unit, defaults={"status":"INSIDE", "registered_by":porteiro})

        provider, _ = ServiceProvider.objects.get_or_create(condominium=condo, provider_name="Eletricista Demo", service_type="Elétrica", unit=unit102, defaults={"company":"Serviços XYZ", "authorized_by":"Síndico", "status":"ACTIVE"})
        ServiceProviderAuditLog.objects.get_or_create(condominium=condo, service_provider=provider, provider_name=provider.provider_name, service_type=provider.service_type, unit=provider.unit, defaults={"status":"ACTIVE", "registered_by":porteiro})

        Package.objects.get_or_create(
            condominium=condo,
            unit=unit101,
            resident=resident1,
            description="Encomenda teste",
            defaults={"delivery_type": "PACKAGE", "store": "Shopee"},
        )

        cat_main, _ = MenuCategory.objects.get_or_create(name="Principal", order=1)
        default_items = [
            ("dashboard", "Dashboard", "/dashboard"),
            ("units", "Unidades", "/units"),
            ("residents", "Moradores", "/residents"),
            ("visitors", "Visitantes", "/visitors"),
            ("visit-logs", "Logs de visita", "/visit-logs"),
            ("packages", "Encomendas", "/packages"),
            ("announcements", "Comunicados", "/announcements"),
            ("incidents", "Ocorrências", "/incidents"),
            ("common-areas", "Áreas comuns", "/common-areas"),
            ("reservations", "Reservas", "/reservations"),
            ("profile", "Perfil", "/profile"),
            ("settings", "Configurações", "/settings"),
        ]
        for i, (key, label, path) in enumerate(default_items, start=1):
            MenuItem.objects.get_or_create(
                key=key,
                defaults={
                    "label": label,
                    "path": path,
                    "category": cat_main,
                    "order": i,
                    "enabled": True,
                    "allowed_roles": ["PLATFORM_ADMIN", "SINDICO", "PORTEIRO", "MORADOR"] if key != "settings" else ["PLATFORM_ADMIN"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed executado com sucesso. Usuários base com senha 123456."))
