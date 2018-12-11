from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET"])
def index(request):
    return render(request, 'main_app/index.html')
