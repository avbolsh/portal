from django.contrib import admin
from .models import User, CertificateRequest

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "uuid", "is_active", "is_staff")
    search_fields = ("username", )
    readonly_fields = ("uuid", "totp_secret")

@admin.register(CertificateRequest)
class CertificateRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "certifacate_type", "status", "created_at")
