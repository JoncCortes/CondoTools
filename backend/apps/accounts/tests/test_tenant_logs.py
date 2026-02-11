from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.condominiums.models import Condominium
from apps.packages.models import Package, PackageAuditLog
from apps.service_providers.models import ServiceProvider, ServiceProviderAuditLog
from apps.units.models import Unit
from apps.visitors.models import Visitor, VisitorAuditLog


class TenantAndAuditFlowsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()

        self.condo_a = Condominium.objects.create(name="Condo A", document="11", address="Rua A")
        self.condo_b = Condominium.objects.create(name="Condo B", document="22", address="Rua B")
        self.unit_a = Unit.objects.create(condominium=self.condo_a, code="101", block="A")
        self.unit_b = Unit.objects.create(condominium=self.condo_b, code="201", block="B")

        self.platform_admin = self.user_model.objects.create_user(
            email="admin@test.com",
            password="123456",
            role=self.user_model.Role.PLATFORM_ADMIN,
            is_staff=True,
        )
        self.porteiro = self.user_model.objects.create_user(
            email="porteiro@test.com",
            password="123456",
            role=self.user_model.Role.PORTEIRO,
            condominium=self.condo_a,
        )

    def auth(self, email, password="123456"):
        response = self.client.post("/api/auth/token/", {"email": email, "password": password}, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_platform_admin_without_active_condo_gets_empty_queryset(self):
        self.auth("admin@test.com")
        response = self.client.get("/api/units/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_package_mark_picked_up_creates_audit_log(self):
        self.auth("porteiro@test.com")
        package = Package.objects.create(
            condominium=self.condo_a,
            unit=self.unit_a,
            description="Caixa",
            status="PENDING",
        )

        response = self.client.post(
            f"/api/packages/{package.id}/mark-picked-up/",
            {"picked_up_by_name": "Maria", "picked_up_quantity": 1},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        package.refresh_from_db()
        self.assertEqual(package.status, "DELIVERED")
        self.assertTrue(PackageAuditLog.objects.filter(package=package, picked_up_by_name="Maria").exists())

    def test_visitor_entry_and_exit_generate_audit_log(self):
        self.auth("porteiro@test.com")
        create_response = self.client.post(
            "/api/visitors/",
            {
                "unit": self.unit_a.id,
                "full_name": "Visitante A",
                "document": "123",
                "authorized_by": "Ana",
                "notes": "Teste",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        visitor_id = create_response.data["id"]
        self.assertTrue(VisitorAuditLog.objects.filter(visitor_id=visitor_id, status="INSIDE").exists())

        exit_response = self.client.post(f"/api/visitors/{visitor_id}/mark-exit/", {}, format="json")
        self.assertEqual(exit_response.status_code, 200)
        self.assertTrue(VisitorAuditLog.objects.filter(visitor_id=visitor_id, status="EXITED").exists())

    def test_service_provider_entry_and_exit_generate_audit_log(self):
        self.auth("porteiro@test.com")
        create_response = self.client.post(
            "/api/service-providers/",
            {
                "unit": self.unit_a.id,
                "provider_name": "Eletricista",
                "company": "Serviços XYZ",
                "document": "789",
                "service_type": "Elétrica",
                "authorized_by": "Síndico",
                "notes": "Troca de lâmpada",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        provider_id = create_response.data["id"]
        self.assertTrue(ServiceProviderAuditLog.objects.filter(service_provider_id=provider_id, status="ACTIVE").exists())

        exit_response = self.client.post(f"/api/service-providers/{provider_id}/mark-exit/", {}, format="json")
        self.assertEqual(exit_response.status_code, 200)
        self.assertTrue(ServiceProviderAuditLog.objects.filter(service_provider_id=provider_id, status="FINISHED").exists())
