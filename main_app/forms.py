from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import password_validation
from django import forms
from users.models import Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length = 254, widget = forms.TextInput(attrs = {'class':'form-control'}))
    password = forms.CharField(label = "Password", widget = forms.PasswordInput(attrs = {'class':'form-control'}))

class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs = {"class":"form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs = {"class":"form-control"}),
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
    field_order = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()
        profile = Profile.objects.get(user=user)
        profile.email = self.cleaned_data['email']
        if commit:
            profile.save()
        return profile