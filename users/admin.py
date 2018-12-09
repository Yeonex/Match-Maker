from django.contrib import admin

# Register your models here.
from .models import Profile, Hobbies

admin.site.register(Profile)
admin.site.register(Hobbies)
