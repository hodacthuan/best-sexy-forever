from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

# Create your views here.
import re
import os


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["email"])
            print(form.cleaned_data["password"])

            return HttpResponseRedirect('/admin/dashboard')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def password(request):
    return render(request, 'password.html')


def register(request):
    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')
