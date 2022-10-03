from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer

from .models import User
from .helpers import check_auth

import jwt
import datetime
# from dateutil.parser import parse as date_parse
# from django.utils import timezone


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
    response = Response({'jwt': token})
    response.set_cookie(key='jwt', value=token)

    return response


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
    user = check_auth(request)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def update_user(request):
    user = check_auth(request)
    if request.data['first_name']:
        user.first_name = request.data['first_name']

    if request.data['last_name']:
        user.last_name = request.data['last_name']

    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)


