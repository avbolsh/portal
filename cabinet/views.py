import pyotp
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from cabinet.models import CertificateRequest
from django.contrib import messages

def login_view(request):

    if request.user.is_authenticated:
        return redirect("cabinet-dashboard")

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
        else:
            messages.error(request, "Неверные логин или пароль")
    return render(request, "cabinet/login.html")

@require_POST
def logout_view(request):
    logout(request)
    return redirect("cabinet-login")
    

@login_required
def dashboard_view(request):
    return render(request, "cabinet/dashboard.html")

@login_required
def profile_view(request):
    return render(request, "cabinet/profile.html")

def totp_view(request):
    if request.method == "POST":
        code = request.POST.get("code")
        user_id = request.session.get("auth_user_id")
        if not user_id:
            return redirect("cabinet-login")
        User = get_user_model()
        user = User.objects.get(id=user_id)

        if not code:
            messages.error(request, "Введите код из приложения")
        else:
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(code):
                login(request, user)
                del request.session["auth_user_id"]
                return redirect("cabinet-dashboard")
            else:
                messages.error(request, "Неверный код")
    return render(request, "cabinet/totp.html")

@login_required
def my_certificates_view(request):
    if request.method == "POST":
        certificate_type = request.POST.get("certificate_type")
        description = request.POST.get("description", "").strip()

        if certificate_type not in dict(CertificateRequest.TYPE_CHOICES):
            messages.error(request, "Неверный тип справки")
        elif certificate_type == "other" and not description:
            messages.error(request, "Для типа «Прочее» необходимо заполнить комментарий")
        else:
            CertificateRequest.objects.create(
                user=request.user,
                certificate_type=certificate_type,
                description=description,
                status="created",
            )
            messages.success(request, "Заявка создана")
            return redirect("cabinet-my-certificates")

    requests = CertificateRequest.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "cabinet/my_certificates.html", {"requests": requests})
