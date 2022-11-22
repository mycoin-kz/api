from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect

from .serializers import UserSerializer, RegisterSerializer

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

import requests

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8080'
    client_class = OAuth2Client


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


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



class GoogleLoginAdapter(APIView):
    permission_classes = [AllowAny]

    CLIENT_ID = '743693342387-bgj30sdiuvhutqnnin9b5ss2l3091p04.apps.googleusercontent.com'
    CLIENT_SECRET = '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'  # Read from a file or environmental variable in a real app
    SCOPE = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/openid'
    REDIRECT_URI = 'https://127.0.0.1:8000/api/auth/google/'


    def post(self, request, *args, **kwargs):
        # return Response('hello there')
        if 'code' not in request.data:
            auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                '&client_id={}&redirect_uri={}&scope={}').format(self.CLIENT_ID, self.REDIRECT_URI, self.SCOPE)
            return Response(auth_uri)
        else:
            auth_code = request.data['code']
            data = {'code': auth_code,
                    'client_id': self.CLIENT_ID,
                    'client_secret': self.CLIENT_SECRET,
                    'redirect_uri': self.REDIRECT_URI,
                    'grant_type': 'authorization_code'
                    }
            r = requests.post('https://oauth2.googleapis.com/token', data=data)
            return Response(r.text)
    
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', '')
        if code == '':
            auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                '&client_id={}&redirect_uri={}&scope={}').format(self.CLIENT_ID, self.REDIRECT_URI, self.SCOPE)
            return Response(auth_uri)
        else:
            data = {'code': code,
                    'client_id': self.CLIENT_ID,
                    'client_secret': self.CLIENT_SECRET,
                    'redirect_uri': self.REDIRECT_URI,
                    'grant_type': 'authorization_code'
                    }
            r = requests.post('https://oauth2.googleapis.com/token', data=data)
            return Response(r.json())
        # return Response('Your data has been passed!')

