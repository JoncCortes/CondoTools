from rest_framework import serializers

from .models import CommonArea


class CommonAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonArea
        fields = "__all__"
