import secrets
import uuid as uuid_lib
import pyotp
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import EmployeeCreateInputSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from cabinet.models import CertificateRequest
from .serializers import CertificateRequestSerializer

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
        if User.objects.filter(uuid=uuid).exists() or User.objects.filter(username=username).exists():
            return Response(
                    {"error": "already_exists", "details": "user with given uuid or username already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                    )
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
                    "uuid": str(user.uuid),
                    "username": user.username,
                    "totp_secret": user.totp_secret,
                    "password": password,
                },
                status=status.HTTP_201_CREATED,
            )


class EmployeeCredentialsResetView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            parsed_uuid = uuid_lib.UUID(str(request.data.get("uuid")))
        except (ValueError, TypeError, AttributeError):
            return Response(
                    {"error": "invalid_input", "details": {"uuid": ["Некорректный UUID."]}},
                    status=status.HTTP_400_BAD_REQUEST,
                    )
        user = User.objects.filter(uuid=parsed_uuid).first()
        if user is None:
            return Response(
                    {"error": "not_found", "details": "user with given uuid does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                    )
        password: str = secrets.token_urlsafe(8)
        user.set_password(password)
        user.totp_secret = pyotp.random_base32()
        user.save(update_fields=["password", "totp_secret"])
        return Response(
                {
                    "uuid": str(user.uuid),
                    "username": user.username,
                    "totp_secret": user.totp_secret,
                    "password": password,
                },
                status=status.HTTP_200_OK,
            )

class CertificateRequestsListView(generics.ListAPIView):
    queryset = CertificateRequest.objects.all()
    serializer_class = CertificateRequestSerializer

class CertificateRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = CertificateRequest.objects.all()
    serializer_class = CertificateRequestSerializer
