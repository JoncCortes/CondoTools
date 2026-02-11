from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from apps.common.permissions import IsPlatformAdmin
from apps.common.viewsets import BaseCondoViewSet
from apps.units.models import Unit

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
        user: User = self.request.user
        if user.is_superuser or user.role == User.Role.PLATFORM_ADMIN:
            return Condominium.objects.all()
        return Condominium.objects.filter(id=user.condominium_id)

    def destroy(self, request, *args, **kwargs):
        condominium = self.get_object()
        if condominium.users.exists() or Unit.objects.filter(condominium=condominium).exists():
            return Response(
                {"detail": "Não é possível excluir este condomínio porque há dados vinculados."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["post"], url_path="wizard/setup")
    def wizard_setup(self, request):
        serializer = WizardSetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data.get("condominium_id"):
            condominium = Condominium.objects.filter(pk=data["condominium_id"]).first()
            if not condominium:
                return Response({"detail": "Condomínio não encontrado."}, status=status.HTTP_404_NOT_FOUND)
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
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="bulk-units")
    def bulk_units(self, request, pk=None):
        condominium = self.get_object()
        serializer = UnitBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = create_units_in_bulk(condominium=condominium, items=serializer.build_units())
        return Response({"detail": f"{created} unidade(s) criadas.", "created": created})
