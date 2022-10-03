from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from .models import User

import jwt


def check_auth(request):
    """
    checks whether the is authorized or not and
    in case of a successful validation returns
    the user object of the current session
    ! IS NOT AN API VIEW
    :param request:
    :return: User object
    """
    token = request.data['jwt']  # get the jwt token from the request cookies

    if not token:
        raise NotAuthenticated('Unauthorized!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])     # get decode the token to get the user id
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token Expired!')

    user = User.objects.get(id=payload['id'])   # fetch the user object from id

    return user



