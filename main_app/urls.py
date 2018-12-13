from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView
from main_app.forms import LoginForm

app_name = 'main_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='sign_up'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
