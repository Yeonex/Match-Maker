from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignupForm, ProfileCreationForm
from users.models import Profile

#If profile hasn't been created, redirect to profile page
@login_required
@require_http_methods(["GET"])
def index(request):
    if(request.user.first_name):
        return render(request, 'main_app/index.html')
    return redirect('main_app:profile')

#Returns profile page or create profile page, or 'creates' the profile
@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileCreationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main_app:index')
        return render(request, 'main_app/create_profile.html', {"form":form})
    if request.user.first_name:
        return render(request, 'main_app/profile.html', {'user':request.user,'profile':profile})
    return render(request, "main_app/create_profile.html", {"form":ProfileCreationForm(instance=profile)})

#Returns the sign up form or signs the user up with the provided info
@require_http_methods(["GET", "POST"])
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')
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