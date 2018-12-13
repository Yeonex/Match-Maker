from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignupForm

@login_required
@require_http_methods(["GET"])
def index(request):
    return render(request, 'main_app/index.html')

@login_required
@require_http_methods(["GET"])
def profile(request):
    return render(request, 'main_app/profile.html')

@require_http_methods(["GET", "POST"])
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main_app:profile')
        return render(request, 'main_app/signup.html', {"form":form})
    return render(request, 'main_app/signup.html', {"form": SignupForm})