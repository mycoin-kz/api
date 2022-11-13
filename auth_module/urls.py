from django.urls import path, include
from . import views

urlpatterns = [
    # path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('profile', views.profile, name='profile'),
    # path('update_user', views.update_user, name='update_user'),
    # path('send_test_mail', views.send_test_mail, name='send_test_mail'),
    
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    
    path('password-reset/<uidb64>/<token>/', views.empty_view, name='password_reset_confirm'),
]
