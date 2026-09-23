from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    uuid = models.UUIDField(
            unique=True, 
            blank=True, 
            null=True, 
            editable=False
            )
    totp_secret = models.CharField(max_length=128, blank=True)

class CertificateRequest(models.Model):
    STATUS_CHOICES = [
            ("created", "Создан"),
            ("processing", "В обработке"),
            ("ready", "Готов"),
            ("rejected", "Отклонен"),
            ]

    TYPE_CHOICES = [
            ("income", "О доходах"),
            ("employment", "С места работы"),
            ("vacation", "Об использованных отпусках"),
            ("other", "Прочее"),
            ]

    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="certificate_requests",
            )
    certificate_type = models.CharField(
            choices=TYPE_CHOICES,
            max_length=50,
            help_text="Тип справки (2-НДФЛ, с места работы и др.)")

    description = models.TextField(
            blank=True,
            help_text="Комментарий сотрудника (период, цель и пр.)")
    status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default="created"
            )
    admin_comment = models.TextField(
            blank=True, 
            max_length=255, 
            help_text="Комментарий ответсвенного сотрудника"
            )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Запрос {self.certificate_type} от {self.user.username}"

