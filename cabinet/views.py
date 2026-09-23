import pyotp
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from cabinet.models import CertificateRequest


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, 
                            username=username, 
                            password=password)
        if user is not None:
            if user.totp_secret:
                request.session["auth_user_id"] = user.id
                return redirect("cabinet-totp")
            login(request, user)
            return redirect("cabinet-dashboard")
    return render(request, "cabinet/login.html")

@require_POST
def logout_view(request):
    logout(request)
    return redirect("cabinet-login")
    

@login_required
def dashboard_view(request):
    return render(request, "cabinet/dashboard.html")

def totp_view(request):

    error = None

    if request.method == "POST":
        code = request.POST.get("code")
        user_id = request.session.get("auth_user_id")
        if not user_id:
            return redirect("cabinet-login")
        User = get_user_model()
        user = User.objects.get(id=user_id)

        if not code:
            error = "Введите код из приложения"
        else:
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(code):
                login(request, user)
                del request.session["auth_user_id"]
                return redirect("cabinet-dashboard")
            else:
                error = "Неверный код"
    return render(request, "cabinet/totp.html", {"error": error})

@login_required
def my_certificates_view(request):
    cert_requests = CertificateRequest.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "cabinet/my_certificates.html", {"cert_requests": cert_requests})
