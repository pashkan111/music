from django.shortcuts import render
from .serializers import CredentialsSerializer



def sign_in(request):
    return render(request, 'accounts/google_login.html')


def log_in(request):
    return render(request, 'accounts/login.html')


# class Creden
