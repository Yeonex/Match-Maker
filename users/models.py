from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OnetoOneField(User, unique = True, on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    email = models.EmailField()
    gender = models.CharField(choices = GENDER_TYPE, max_length=1)

class Hobbies(models.Model):
    name = models.CharField(max_length=200)

# Model Options
GENDER_TYPE = (
    ('M', 'Male'),
    ('F', 'Female')
)
