from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import password_validation
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length = 254, widget = forms.TextInput(attrs = {'class':'form-control'}))
    password = forms.CharField(label = "Password", widget = forms.PasswordInput(attrs = {'class':'form-control'}))

class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs = {"class":"form-control"}),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs = {"class":"form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs = {"class":"form-control"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )