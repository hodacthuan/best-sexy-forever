from django.shortcuts import render

# Create your views here.
import re
import os


def login(request):
    return render(request, 'login.html')
