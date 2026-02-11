from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        PLATFORM_ADMIN = "PLATFORM_ADMIN", "Platform Admin"
        SINDICO = "SINDICO", "Síndico"
        PORTEIRO = "PORTEIRO", "Porteiro"
        MORADOR = "MORADOR", "Morador"

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MORADOR)
    condominium = models.ForeignKey(
        "condominiums.Condominium",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
