from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('current/', views.current_user_info, name='current_user_info'),
    path('<int:user_id>/', views.user_info, name='user_info'),
    path('like/<int:user_id>/', views.liked_user, name='liked_user'), #liked_user
    path('liked/', views.get_liked_users, name='get_liked_users'),
    path('hobbies/', views.hobbies, name='hobbies')
]
