from rest_framework import serializers
from .models import WasteBatch


# ✅ основной сериализатор
class WasteBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBatch
        fields = "__all__"


# ✅ создание партии
class EducatorBatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBatch
        fields = [
            "type",
            "quantity",
            "unit",
        ]


# ✅ обновление партии
class EducatorBatchUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteBatch
        fields = [
            "type",
            "quantity",
            "unit",
        ]


# ✅ история статусов (заглушка, чтобы не падало)
class BatchStatusHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField()
    changed_at = serializers.DateTimeField()


# ✅ продление токена
class ExtendTokenSerializer(serializers.Serializer):
    expires_at = serializers.DateTimeField()
    signature_token = serializers.CharField(required=False)


# ✅ заблокированные попытки
class BlockedAttemptSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField()