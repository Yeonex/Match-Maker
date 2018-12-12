from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Profile, Hobbies
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


# Create your views here.
@require_http_methods(["GET", "POST"])
def index(request):
    #get and post in index for posting
    if request.method == "GET":
        json = []
        users = User.objects.all()
        for user in users:
            j = {
                "first_name" : user.first_name,
                "last_name" : user.last_name,
                "email" : user.email,
                "profile_pic" : user.profile.profile_pic.url,
                "gender" : user.profile.gender,
                "date_of_birth" : user.profile.date_of_birth,
                "hobbies" : "TODO"
            }
            json.append(j)
    return JsonResponse(json, safe=False)

@require_http_methods(["GET"])
def user_info(request, user_id):
    #get request for user
    if request.method == "GET":
        user = get_object_or_404(User, pk=user_id)
        json = {
            "first_name" : user.first_name,
            "last_name" : user.last_name,
            "email" : user.email,
            "profile_pic" : user.profile.profile_pic.url,
            "gender" : user.profile.gender,
            "date_of_birth" : user.profile.date_of_birth,
            "hobbies" : "TODO"
        }
    return JsonResponse(json, safe=False)

def get_liked_users(request):
    #Gets all users liked by this account
    return HttpResponse("Liked users returned")

def liked_user(request, user_id):
    #Like user
    return HttpResponse("Liked " + str(user_id))
