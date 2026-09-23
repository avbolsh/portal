from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, 
                            username=username, 
                            password=password)
        if user is not None:
            login(request, user)
            return redirect("cabinet-dashboard")
    return render(request, "cabinet/login.html")
    

@login_required
def dashboard_view(request):
    return render(request, "cabinet/dashboard.html")
