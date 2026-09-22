from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, blank=True, null=True)
    totp_secret = models.CharField(max_length=128, blank=True)

