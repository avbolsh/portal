from django.urls import path
from .views import login_view, logout_view, dashboard_view, totp_view

urlpatterns = [
        path("login/", login_view, name="cabinet-login"),
        path("logout", logout_view, name="cabinet-logout"),
        path("", dashboard_view, name="cabinet-dashboard"),
        path("totp/", totp_view, name="cabinet-totp"),
        ]
