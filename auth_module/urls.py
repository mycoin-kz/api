from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('profile', views.profile, name='profile'),
    
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('google/', views.GoogleLoginAdapter.as_view(), name='google_login'),
    path('google-code/', views.GoogleLogin.as_view(), name='google_login'),
    path('accounts', include('allauth.urls'), name='socialaccount_signup'),
    
    path('password-reset/<uidb64>/<token>/', views.empty_view, name='password_reset_confirm'),
]
