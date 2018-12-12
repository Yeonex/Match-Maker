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
        current_user = request.user
        users = User.objects.all()
        for user in users:
            hobbies = []
            liked = False
            if current_user in user.profile.profile_connections.all():
                liked = True
            for hobby in user.profile.hobbies.all():
                hobbies.append(str(hobby))
            j = {
                "id" : user.id,
                "first_name" : user.first_name,
                "last_name" : user.last_name,
                "email" : user.email,
                "profile_pic" : user.profile.profile_pic.url,
                "gender" : user.profile.gender,
                "date_of_birth" : user.profile.date_of_birth,
                "hobbies" : hobbies,
                "liked" : "True"
            }
            json.append(j)
    return JsonResponse(json, safe=False)

@require_http_methods(["GET"])
def user_info(request, user_id):
    #get request for user
    if request.method == "GET":
        user = get_object_or_404(User, pk=user_id)
        hobbies = []
        for hobby in user.profile.hobbies.all():
            hobbies.append(str(hobby))
        json = {
            "first_name" : user.first_name,
            "last_name" : user.last_name,
            "email" : user.email,
            "profile_pic" : user.profile.profile_pic.url,
            "gender" : user.profile.gender,
            "date_of_birth" : user.profile.date_of_birth,
            "hobbies" : hobbies
            }
    return JsonResponse(json, safe=False)

def get_liked_users(request):
    #Gets all users liked by this account
    return HttpResponse("Liked users returned")

@require_http_methods(["PUT"])
def liked_user(request, user_id):
    #Like user
    if request.method == "PUT":
        current_user = request.user
        user_to_like = user = get_object_or_404(User, pk=user_id)
        if user_to_like in current_user.profile.profile_connections:
            current_user.profile.profile_connections.remove(user_to_like)
        else:
            current_user.profile.profile_connections.add(user_to_like)

    return HttpResponse("Success")
