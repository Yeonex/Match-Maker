from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Model Options
GENDER_TYPE = (
    ('M', 'Male'),
    ('F', 'Female')
)

# Create your models here.
class Hobbies(models.Model):
    name = models.CharField(max_length=200)

class Profile(models.Model):
    user = models.OneToOneField(User, unique = True, on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'profile_pics/', default = 'pic_folder/None/no-img.jpg')
    email = models.EmailField()
    gender = models.CharField(choices = GENDER_TYPE, max_length=1)
    date_of_birth = models.DateField()
    hobbies = models.ManyToManyField('Hobbies')
    profile_requests = models.ManyToManyField('self')
    profile_connections = models.ManyToManyField('self')

#Creates an instance of profile whenever a user object is created
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
