from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Profile, Hobbies
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from datetime import date

def getUserDict(request, user):
    current_user = request.user
    hobbies = []
    liked = False
    if current_user.profile in user.profile.profile_connections.all():
        liked = True
    hobbies = []
    for hobby in user.profile.hobbies.all():
        hobbies.append({"value" : hobby.id, "name" : str(hobby)})
    return {
        "id" : user.id,
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "email" : user.email,
        "profile_pic" : user.profile.profile_pic.url if user.profile.profile_pic else '',
        "gender" : user.profile.gender,
        "date_of_birth" : user.profile.date_of_birth,
        "result" : hobbies,
        "liked" : liked
    }

@require_http_methods(["GET", "POST"])
def index(request):
    #get and post in index for posting
    if request.method == "GET":
        if 'min_age' in request.GET:
            try:
                min_age = int(request.GET['min_age'])
            except:
                min_age = 0
        else:
            min_age = 0
        if 'max_age' in request.GET:
            try:
                max_age = int(request.GET['max_age'])
            except:
                max_age = 10000
        else:
            max_age = 10000
        if 'gender' in request.GET and (request.GET['gender'] == "M" or request.GET['gender'] == "F"):
            gender = request.GET['gender'].capitalize()
        else:
            gender = None
        json = []
        current_user = request.user
        users = User.objects.all()
        for user in users:
            dob = user.profile.date_of_birth
            age = date.today().year - dob.year
            user_gender = user.profile.gender
            if user.id == current_user.id:
                continue
            if min_age <= age <= max_age:
                if gender is None:
                    j = getUserDict(request, user)
                    json.append(j)
                else:
                    if gender == user_gender:
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
        hobbies.append({"value" : hobby.id, "name" : str(hobby)})
    json = {
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "email" : user.email,
        "profile_pic" : user.profile.profile_pic.url,
        "gender" : user.profile.gender,
        "date_of_birth" : user.profile.date_of_birth,
        "result" : hobbies,
        "liked_count" : user.profile.profile_connections.count()
        }
    return JsonResponse(json, safe=False)

@require_http_methods(["GET", "PUT"])
def current_user_info(request):
    if request.method == "PUT":
        request.PUT = QueryDict(request.body)
        form = ProfileCreationForm(request.PUT, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({"status":"success"})
        return JsonResponse(form.errors, safe=False, status=400)
    return JsonResponse(getUserDict(request, request.user), safe=False)

def get_liked_users(request):
    #Gets all users liked by this account
    current_user = request.user

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
def hobbies(request):
    json = []
    for hobby in Hobbies.objects.all():
        json.append({'value':hobby.id, 'name':hobby.name})
    return JsonResponse(json, safe=False)
