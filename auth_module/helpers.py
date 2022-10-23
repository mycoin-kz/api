from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from .models import User
from django.http.request import HttpRequest
import jwt


def check_auth(request: HttpRequest):
    """
    checks whether the is authorized or not and
    in case of a successful validation returns
    the user object of the current session
    ! IS NOT AN API VIEW
    :param request:
    :return: User object
    """
    token = None  # get the jwt token from the request cookies
    # print(f'token: {token}')
    print(f'cookie: {request.COOKIES}')

    if 'HTTP_AUTHORIZATION' in request.META:
        token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    elif 'jwt' in request.COOKIES:
        token = request.COOKIES['jwt']
    elif 'jwt' in request.data:
        token = request.data['jwt']
    if not token:
        raise NotAuthenticated('Unauthorized!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])     # get decode the token to get the user id
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token Expired!')

    user = User.objects.get(id=payload['id'])   # fetch the user object from id

    return user



