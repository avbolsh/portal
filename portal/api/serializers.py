from rest_framework import serializers
from django.contrib.auth import get_user_model
from cabinet.models import CertificateRequest

User = get_user_model()

class EmployeeCreateInputSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    username = serializers.CharField()

class CertificateRequestSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(source="user.uuid", read_only=True)
    
    class Meta:
        model = CertificateRequest
        fields = [
                "id",
                "user_uuid",
                "certificate_type",
                "description",
                "status",
                "created_at",
                "updated_at",
                "admin_comment",
                ]

        read_only_fields = [
                "id",
                "user_uuid",
                "certificate_type",
                "created_at",
                "updated_at",
                ]
