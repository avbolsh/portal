from django.urls import path
from .views import EmployeeCreateView, PingView

urlpatterns = [
        path("ping", PingView.as_view(), name="api-ping"),
        path("employees/", EmployeeCreateView.as_view(), name="api-employee-create"),
        ]
