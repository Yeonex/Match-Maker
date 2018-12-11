from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Hobbies
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    #get and post in index for posting
    return HttpResponse("Hello, world. You're at the users index.")

def user_info(request, user_id):
    #get request for user
    return HttpResponse("User returned here")

def get_liked_users(request):
    #Gets all users liked by this account
    return HttpResponse("Liked users returned")

def liked_user(request, user_id_to_like):
    #Like user
    return HttpResponse("Like a user")
