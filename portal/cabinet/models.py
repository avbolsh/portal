from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    uuid = models.UUIDField(
            unique=True,
            blank=True,
            null=True,
            editable=False,
            verbose_name="UUID",
            )
    totp_secret = models.CharField(max_length=128, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

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
            verbose_name="Сотрудник",
            )
    certificate_type = models.CharField(
            choices=TYPE_CHOICES,
            max_length=50,
            verbose_name="Тип справки",
            help_text="Тип справки (2-НДФЛ, с места работы и др.)")

    description = models.TextField(
            blank=True,
            verbose_name="Комментарий сотрудника",
            help_text="Комментарий сотрудника (период, цель и пр.)")
    status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default="created",
            verbose_name="Статус",
            )
    admin_comment = models.TextField(
            blank=True,
            max_length=255,
            verbose_name="Комментарий ответственного",
            help_text="Комментарий ответсвенного сотрудника"
            )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка на справку"
        verbose_name_plural = "Заявки на справки"

    def __str__(self):
        return f"Запрос {self.certificate_type} от {self.user.username}"

