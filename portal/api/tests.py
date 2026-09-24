import uuid as uuid_lib

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class EmployeeApiTests(APITestCase):
    def setUp(self):
        self.service_user = User.objects.create_user(username="service")
        token = Token.objects.create(user=self.service_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_employee(self):
        response = self.client.post(
                reverse("api-employee-create"),
                {"uuid": str(uuid_lib.uuid4()), "username": "ivanov"},
                format="json",
                )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "ivanov")
        self.assertIn("password", response.data)
        self.assertIn("totp_secret", response.data)

    def test_create_employee_with_invalid_uuid(self):
        response = self.client.post(
                reverse("api-employee-create"),
                {"uuid": "not-a-uuid", "username": "ivanov"},
                format="json",
                )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "invalid_input")

    def test_create_duplicate_returns_already_exists(self):
        existing_uuid = str(uuid_lib.uuid4())
        User.objects.create_user(username="ivanov", uuid=existing_uuid)
        response = self.client.post(
                reverse("api-employee-create"),
                {"uuid": existing_uuid, "username": "petrov"},
                format="json",
                )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "already_exists")

    def test_create_duplicate_username_returns_already_exists(self):
        User.objects.create_user(username="ivanov")
        response = self.client.post(
                reverse("api-employee-create"),
                {"uuid": str(uuid_lib.uuid4()), "username": "ivanov"},
                format="json",
                )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "already_exists")

    def test_reset_credentials(self):
        user_uuid = uuid_lib.uuid4()
        user = User.objects.create_user(
                username="ivanov",
                password="old-password",
                uuid=user_uuid,
                totp_secret="OLDSSECRET",
                )
        response = self.client.post(
                reverse("api-employee-reset"),
                {"uuid": str(user_uuid)},
                format="json",
                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "ivanov")
        user.refresh_from_db()
        self.assertNotEqual(response.data["password"], "old-password")
        self.assertNotEqual(user.totp_secret, "OLDSSECRET")
        self.assertTrue(user.check_password(response.data["password"]))

    def test_reset_unknown_uuid_returns_404(self):
        response = self.client.post(
                reverse("api-employee-reset"),
                {"uuid": str(uuid_lib.uuid4())},
                format="json",
                )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "not_found")

    def test_reset_invalid_uuid_returns_400(self):
        response = self.client.post(
                reverse("api-employee-reset"),
                {"uuid": "garbage"},
                format="json",
                )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "invalid_input")

    def test_requires_authentication(self):
        self.client.credentials()
        response = self.client.post(
                reverse("api-employee-reset"),
                {"uuid": str(uuid_lib.uuid4())},
                format="json",
                )
        self.assertEqual(response.status_code, 401)
