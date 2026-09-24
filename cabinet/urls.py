from django.urls import path
from .views import login_view, logout_view, dashboard_view, totp_view, my_certificates_view, profile_view, certificate_detail_view

urlpatterns = [
        path("login/", login_view, name="cabinet-login"),
        path("logout", logout_view, name="cabinet-logout"),
        path("", dashboard_view, name="cabinet-dashboard"),
        path("totp/", totp_view, name="cabinet-totp"),
        path("my-certificates/", my_certificates_view, name="cabinet-my-certificates"),
        path("my-certificates/<int:pk>/", certificate_detail_view, name="cabinet-certificate-detail"),
        path("profile", profile_view, name="cabinet-profile"),
        ]
