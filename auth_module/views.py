from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, LoginSerializer, RegisterSerializer

from .models import User
from .helpers import check_auth

import jwt
import datetime

from django.contrib.auth import authenticate, login

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dateutil.parser import parse as date_parse
# from django.utils import timezone


# class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
#     client_class = OAuth2Client


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


# class LoginView(APIView):
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny]
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         email = request.data['email']
#         password = request.data['password']
#         user = authenticate(username=email, password=password)
#         if user is not None:
#             login(request._request)
#             serializer = UserSerializer(user)
#             return Response(serializer.data)
#         raise AuthenticationFailed()


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data)
        

@api_view(['POST'])
def login(request):
    """
    Takes username and password as
    parameters, logs in the user and
    returns an authorization token.
    If the user is not registered,
    returns 404 response and shows an appropriate message

    :param request:
    :return:
    """
    email = request.data['email']
    password = request.data['password']
    user = User.objects.get(email=email)

    if not user.check_password(password):
        raise AuthenticationFailed('Password is incorrect!')

    token = jwt.encode(
        {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        },
        'secret',
        algorithm='HS256'
    )
    return Response({'jwt': token})


@api_view(['POST'])
def register(request):
    """
    Takes username, email and password as parameters,
    and registers the user after validation.
    In case of failed validation (username already in use, etc.)
    responds with an appropriate message.

    :param request:
    :return:
    """
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def profile(request):
    """
    Returns the basic info about the logged user
    :param request:
    :return:
    """
    try:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    except:
        raise AuthenticationFailed()


# @api_view(['POST'])
# def update_user(request):
#     user = check_auth(request)
#     if request.data['first_name']:
#         user.first_name = request.data['first_name']

#     if request.data['last_name']:
#         user.last_name = request.data['last_name']

#     user.save()
#     serializer = UserSerializer(user)
#     return Response(serializer.data)


@api_view(['GET'])
def empty_view(request, uidb64, token):
    return Response('empty view')


