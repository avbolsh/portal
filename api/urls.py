from django.urls import path
from .views import EmployeeCreateView, PingView, CertificateRequestsListView, CertificateRequestDetailView, EmployeeCredentialsResetView 

urlpatterns = [
        path("ping/", PingView.as_view(), name="api-ping"),
        path("employees/", EmployeeCreateView.as_view(), name="api-employee-create"),
        path("employees/reset/", EmployeeCredentialsResetView.as_view(), name="api-employee-reset"),
        path("certificates/", CertificateRequestsListView.as_view(), name="api-certificate-list"),
        path("certificates/<int:pk>/", CertificateRequestDetailView.as_view(), name="api-certificate-detail"),
        ]
