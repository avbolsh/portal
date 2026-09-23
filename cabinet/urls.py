from django.urls import path
from .views import login_view, dashboard_view

urlpatterns = [
        path("login/", login_view, name="cabinet-login"),
        path("", dashboard_view, name="cabinet-dashboard"),
        ]
