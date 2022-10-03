from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('update_user', views.update_user, name='update_user'),
]
