from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from apps.common.permissions import IsPlatformAdmin
from apps.common.viewsets import BaseCondoViewSet

from .models import Condominium
from .serializers import (
    CondominiumSerializer,
    UnitBulkCreateSerializer,
    WizardSetupSerializer,
    create_syndic,
    create_units_in_bulk,
)


class CondominiumViewSet(BaseCondoViewSet):
    queryset = Condominium.objects.all()
    serializer_class = CondominiumSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "document"]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy", "wizard_setup", "bulk_units"}:
            return [permissions.IsAuthenticated(), IsPlatformAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        user: User = self.request.user
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            return Condominium.objects.all()
        return Condominium.objects.filter(id=user.condominium_id)

    @action(detail=False, methods=["post"], url_path="wizard/setup")
    def wizard_setup(self, request):
        serializer = WizardSetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data.get("condominium_id"):
            condominium = Condominium.objects.get(pk=data["condominium_id"])
        else:
            condominium = Condominium.objects.create(
                name=data["name"],
                document=data.get("document", ""),
                address=data.get("address", ""),
            )

        syndic = create_syndic(
            condominium=condominium,
            first_name=data["syndic_first_name"],
            last_name=data.get("syndic_last_name", ""),
            email=data["syndic_email"],
            password=data["syndic_password"],
        )

        return Response(
            {
                "detail": "Condomínio e primeiro síndico criados com sucesso.",
                "condominium_id": condominium.id,
                "syndic_id": syndic.id,
            },
            status=201,
        )

    @action(detail=True, methods=["post"], url_path="bulk-units")
    def bulk_units(self, request, pk=None):
        condominium = self.get_object()
        serializer = UnitBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = create_units_in_bulk(condominium=condominium, items=serializer.build_units())
        return Response({"detail": f"{created} unidade(s) criadas.", "created": created})
