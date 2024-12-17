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
from decouple import config

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class GoogleLogin(
    SocialLoginView
):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = config("FRONTEND_URL", "http://localhost:8080")
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


@api_view(["POST"])
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


@api_view(["GET", "POST"])
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


@api_view(["GET"])
def empty_view(request, uidb64, token):
    return Response("empty view")


class GoogleLoginAdapter(APIView):
    permission_classes = [AllowAny]

    CLIENT_ID = config("GOOGLE_CLIENT_ID", "")
    CLIENT_SECRET = config("GOOGLE_SECRET_KEY", "")
    REDIRECT_URI = config("GOOGLE_REDIRECT_URI", "")  # For web flow
    FRONT_REDIRECT = config("GOOGLE_FRONTEND_REDIRECT", "")  # For web flow

    def post(self, request, *args, **kwargs):
        """
        Universal endpoint that handles both web and mobile authentication:
        - For mobile: Expects an ID token in the request body
        - For web: Handles the OAuth2 code flow
        """
        # Mobile flow - direct token verification
        id_token = request.data.get("id_token")
        if id_token:
            return self._handle_mobile_flow(id_token)

        # Web flow - OAuth2 code exchange
        auth_code = request.data.get("code")
        if auth_code:
            return self._handle_web_flow(auth_code)

        return Response(
            {"error": "Either id_token (mobile) or code (web) is required"}, status=400
        )

    def _handle_mobile_flow(self, id_token):
        """Handle mobile authentication with direct token verification"""
        try:
            # Verify the token with Google
            google_verify_url = (
                f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
            )
            response = requests.get(google_verify_url)
            if response.status_code != 200:
                return Response({"error": "Invalid token"}, status=401)

            token_info = response.json()

            # Verify that the token was issued for your app
            if token_info.get("aud") != self.CLIENT_ID:
                return Response({"error": "Token not issued for this app"}, status=401)

            return self._handle_successful_auth(token_info)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def _handle_web_flow(self, auth_code):
        """Handle web authentication with OAuth2 code flow"""
        try:
            # Exchange code for token
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "code": auth_code,
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
                "redirect_uri": self.REDIRECT_URI,
                "grant_type": "authorization_code",
            }

            response = requests.post(token_url, data=data)
            if response.status_code != 200:
                return Response({"error": "Failed to exchange code"}, status=401)

            tokens = response.json()

            # Verify ID token
            id_token = tokens.get("id_token")
            if not id_token:
                return Response({"error": "No ID token in response"}, status=401)

            # Verify the token
            verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
            verify_response = requests.get(verify_url)
            if verify_response.status_code != 200:
                return Response({"error": "Invalid ID token"}, status=401)

            token_info = verify_response.json()
            return self._handle_successful_auth(token_info)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def _handle_successful_auth(self, token_info):
        """Common handler for successful authentication"""
        try:
            # Here you would typically:
            # 1. Get or create a user based on the Google ID (token_info.sub)
            # 2. Generate your app's authentication token
            # 3. Return the token and any other necessary user info

            return Response(
                {"token_info": token_info, "message": "Successfully authenticated"}
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def get(self, request, *args, **kwargs):
        """Optional: Handle initial web OAuth flow"""
        if request.GET.get("web_flow") == "true":
            auth_uri = (
                "https://accounts.google.com/o/oauth2/v2/auth?"
                "response_type=code"
                f"&client_id={self.CLIENT_ID}"
                f"&redirect_uri={self.REDIRECT_URI}"
                "&scope=email profile"
            )
            return Response({"auth_url": auth_uri})

        return Response(
            {"error": "GET method is only supported for web flow initialization"},
            status=405,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
