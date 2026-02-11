from rest_framework import serializers

from apps.common.serializers import CondoScopedSerializerMixin

from .models import CommonArea


class CommonAreaSerializer(CondoScopedSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CommonArea
        fields = "__all__"
