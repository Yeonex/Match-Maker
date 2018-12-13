from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

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
    if request.user.is_authenticated():
        redirect('home')
    return HttpResponse("Signup page TODO")
