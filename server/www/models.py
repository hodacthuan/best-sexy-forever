from django.db import models
from django import forms

# Create your models here.


class LoginForm(forms.Form):
    email = forms.CharField(label='Your name', max_length=100)
    password = forms.CharField(label='Your password', max_length=100)
