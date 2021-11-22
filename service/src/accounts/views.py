from django.shortcuts import render


def sign_in(request):
    return render(request, "accounts/google_login.html")


def register_page(request):
    return render(request, "accounts/register.html")


def login_page(request):
    return render(request, "accounts/login.html")
