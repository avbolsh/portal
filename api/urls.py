from django.urls import path
from .views import EmployeeCreateView, PingView, CertificateRequestsListView, CertificateRequestDetailView 

urlpatterns = [
        path("ping/", PingView.as_view(), name="api-ping"),
        path("employees/", EmployeeCreateView.as_view(), name="api-employee-create"),
        path("certificates/", CertificateRequestsListView.as_view(), name="api-certificate-list"),
        path("certificates/<int:pk>/", CertificateRequestDetailView.as_view(), name="api-certificate-detail"),
        ]
