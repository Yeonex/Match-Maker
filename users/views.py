from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Profile, Hobbies
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage

#from django.views.decorators.csrf import csrf_exempt

def getUserDict(request, user):
    current_user = request.user
    hobbies = []
    liked = False
    if current_user.profile in user.profile.profile_connections.all():
        liked = True
    for hobby in user.profile.hobbies.all():
        hobbies.append(str(hobby))
    return {
        "id" : user.id,
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "email" : user.email,
        "profile_pic" : user.profile.profile_pic.url if user.profile.profile_pic else '',
        "gender" : user.profile.gender,
        "date_of_birth" : user.profile.date_of_birth,
        "hobbies" : hobbies,
        "liked" : liked
    }

@require_http_methods(["GET", "POST"])
def index(request):
    #get and post in index for posting
    if request.method == "GET":
        json = []
        current_user = request.user
        users = User.objects.all()
        for user in users:
            if user.id == current_user.id:
                continue
            j = getUserDict(request, user)
            json.append(j)
        return JsonResponse({"current_user":getUserDict(request, current_user),"others":json}, safe=False)
    return HttpResponse("POST todo")

@require_http_methods(["GET"])
def user_info(request, user_id):
    #get request for user
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
        "hobbies" : hobbies,
        "liked_count" : user.profile.profile_connections.count()
        }
    return JsonResponse(json, safe=False)

@require_http_methods(["GET", "PUT"])
def current_user_info(request):
    #if request.method == "PUT":

    return JsonResponse(getUserDict(request, request.user), safe=False)

def get_liked_users(request):
    #Gets all users liked by this account
    return HttpResponse("Liked users returned")


@require_http_methods(["PUT"])
def liked_user(request, user_id):
    #Like user
    current_user = request.user
    user_to_like = get_object_or_404(User, pk=user_id)
    if user_to_like.profile in current_user.profile.profile_connections.all():
        current_user.profile.profile_connections.remove(user_to_like.profile)
        current_user.save()
    else:
        current_user.profile.profile_connections.add(user_to_like.profile)
        current_user.save()

        email = EmailMessage(
        'You have a new match!',
        'Congratulations, {} you have been liked by {}'.format(user_to_like.first_name, current_user.first_name),
        'apikey',
        [user_to_like.profile.email])
        email.send()
    return HttpResponse("Success")

@require_http_methods(["GET"])
def filter_by_age(request, max_age, min_age):
    json = []
    current_user = request.user
    users = User.objects.all()
    for user in users:
        age = Profile.get_age(user.id)
        if min_age <= age <= max_age:
            j = getUserDict(request, user)
            json.append(j)

    return JsonResponse({"current_user": getUserDict(request, current_user), "others": json}, safe=False)

@require_http_methods(["GET"])
def hobbies(request):
    json = []
    for hobby in Hobbies.objects.all():
        json.append({'value':hobby.id, 'name':hobby.name})
    return JsonResponse(json, safe=False)