from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, QueryDict
from .models import Profile, Hobbies
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from datetime import date
from main_app.forms import ProfileCreationForm

#Return a dict representing the passed user, relative to the current user
def getUserDict(request, user, hobbyIDs=False):
    current_user = request.user
    hobbies = []
    liked = False
    if current_user.profile in user.profile.profile_connections.all():
        liked = True
    hobbies = []
    for hobby in user.profile.hobbies.all():
        if hobbyIDs:
            hobbies.append({"value" : hobby.id, "name" : str(hobby)})
        else:
            hobbies.append(str(hobby))
    return {
        "id" : user.id,
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "email" : user.email,
        "profile_pic" : user.profile.profile_pic.url if user.profile.profile_pic else '',
        "gender" : user.profile.gender,
        "date_of_birth" : user.profile.date_of_birth,
        "bio": user.profile.bio,
        "hobbies" : hobbies,
        "liked" : liked
    }

#The index simply returns the current user and a list of other users with profiles
@require_http_methods(["GET"])
def index(request):
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
        if user.id == current_user.id:
            continue
        if user.first_name:
            dob = user.profile.date_of_birth
            age = abs(date.today().year - dob.year)
            user_gender = user.profile.gender
            if min_age <= age <= max_age:
                if gender is None:
                    j = getUserDict(request, user)
                    json.append(j)
                else:
                    if gender == user_gender:
                        j = getUserDict(request, user)
                        json.append(j)
    return JsonResponse({"current_user":getUserDict(request, current_user),"others":json}, safe=False)

#Simply returns a dict for the given user
@require_http_methods(["GET"])
def user_info(request, user_id):
    #get request for user
    user = get_object_or_404(User, pk=user_id)
    return JsonResponse(getUserDict(request, user), safe=False)

#Returns info about the current user, or updates the info
@require_http_methods(["GET", "PUT"])
def current_user_info(request):
    if request.method == "PUT":
        profile = Profile.objects.get(user=request.user)
        request.PUT = QueryDict(request.body)
        form = ProfileCreationForm(request.PUT, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({"status":"success", "user":getUserDict(request, profile.user, True)})
        return JsonResponse(form.errors, safe=False, status=400)
    return JsonResponse(getUserDict(request, request.user, True), safe=False)

#Toggles the liked status of the given user from the current user
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
        [user_to_like.email])
        email.send()
    return HttpResponse("Success")

#Returns the list of hobbies to be included in forms
@require_http_methods(["GET"])
def hobbies(request):
    json = []
    for hobby in Hobbies.objects.all():
        json.append({'value':hobby.id, 'name':hobby.name})
    return JsonResponse(json, safe=False)
