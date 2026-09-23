from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeCreateInputSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    username = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_uuid(self, value):
        if User.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("UUID already exists")
        return value
