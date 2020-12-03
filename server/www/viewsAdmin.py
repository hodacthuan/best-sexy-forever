from django.shortcuts import render

# Create your views here.
import re
import os


def login(request):
    return render(request, 'login.html')


def password(request):
    return render(request, 'password.html')


def register(request):
    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')
