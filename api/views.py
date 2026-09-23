import secrets
import pyotp
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import EmployeeCreateInputSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()


class PingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})

class EmployeeCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EmployeeCreateInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response (
                    {"error": "invalid_input", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                    )
        uuid = serializer.validated_data["uuid"]
        username = serializer.validated_data["username"]
        password: str = secrets.token_urlsafe(8)
        totp_secret: str  = pyotp.random_base32()

        user = User.objects.create_user(
                username=username,
                password=password,
                uuid=uuid,
                totp_secret=totp_secret,
                )
        return Response(
                {
                    "uuid": user.uuid,
                    "username": user.username,
                    "totp_secret": user.totp_secret,
                    "password": password,
                },
                status=status.HTTP_201_CREATED,
            )



