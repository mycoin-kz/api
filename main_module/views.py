from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.permissions import IsAuthenticated

from auth_module.helpers import check_auth
from main_module.models import Watchlist
from .serializers import WatchlistSerializer
from django.db.utils import IntegrityError

@api_view(['GET'])
def index(request):
    return Response(data='index endpoint!')


@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def watchlist(request):
    if request.method == 'GET':
        serializer = WatchlistSerializer(request.user.watchlist, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        try: 
            watchlist_obj = Watchlist(user=request.user, token=request.data['token'])
            watchlist_obj.save()
        except IntegrityError:
            pass
        serializer = WatchlistSerializer(request.user.watchlist, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_watchlist(request, token_id):
    try:
        watchlist = Watchlist.objects.get(user=request.user, token=token_id)
        watchlist.delete()
    except:
        pass
    serializer = WatchlistSerializer(request.user.watchlist, many=True)
    return Response(serializer.data)


