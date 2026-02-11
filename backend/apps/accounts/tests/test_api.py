from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.condominiums.models import Condominium
from apps.units.models import Unit


class AuthAndPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        self.condo_a = Condominium.objects.create(name="A", document="1", address="Rua A")
        self.condo_b = Condominium.objects.create(name="B", document="2", address="Rua B")

        self.sindico = self.user_model.objects.create_user(
            email="sindico@test.com", password="123456", role="SINDICO", condominium=self.condo_a
        )
        self.porteiro = self.user_model.objects.create_user(
            email="porteiro@test.com", password="123456", role="PORTEIRO", condominium=self.condo_a
        )

        Unit.objects.create(condominium=self.condo_a, code="101", block="A")
        Unit.objects.create(condominium=self.condo_b, code="201", block="B")

    def auth(self, email, password="123456"):
        resp = self.client.post("/api/auth/token/", {"email": email, "password": password}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")

    def test_jwt_login_with_email(self):
        response = self.client.post(
            "/api/auth/token/",
            {"email": "sindico@test.com", "password": "123456"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_condominium_filter_on_units(self):
        self.auth("sindico@test.com")
        response = self.client.get("/api/units/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["code"], "101")

    def test_doorman_cannot_create_unit(self):
        self.auth("porteiro@test.com")
        response = self.client.post("/api/units/", {"code": "999", "block": "Z"}, format="json")
        self.assertEqual(response.status_code, 403)
