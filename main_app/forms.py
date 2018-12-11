from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length = 254, widget = forms.TextInput(attrs = {'class':'form-control'}))
    password = forms.CharField(label = "Password", widget = forms.PasswordInput(attrs = {'class':'form-control'}))
    print("test")