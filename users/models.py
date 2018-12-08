from django.db import models
from django.contrib.auth.models import User

# Model Options
GENDER_TYPE = (
    ('M', 'Male'),
    ('F', 'Female')
)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, unique = True, on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    email = models.EmailField()
    gender = models.CharField(choices = GENDER_TYPE, max_length=1)
    date_of_birth = models.DateField()
    hobbies = models.ManyToMany('Hobbies')
    requests = models.ManyToMany('Profile')
    connections = models.ManyToMany('Profile')

class Hobbies(models.Model):
    name = models.CharField(choices = HOBBIES_LIST, max_length=200)

#Creates an instance of profile whenever a user object is created
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
