from rest_framework.response import Response
from rest_framework.decorators import api_view
from auth_module.helpers import check_auth
from main_module.models import Watchlist
from .serializers import WatchlistSerializer
from django.db.utils import IntegrityError
from rest_framework import status

@api_view(['GET'])
def index(request):
    return Response(data='index endpoint!')


@api_view(['POST', 'GET', 'DELETE'])
def watchlist(request):
    if request.method == 'GET':
        user = check_auth(request)
        serializer = WatchlistSerializer(user.watchlist, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        user = check_auth(request)
        try: 
            watchlist_obj = Watchlist(user=user, token=request.data['token'])
            watchlist_obj.save()
        except IntegrityError:
            pass
        serializer = WatchlistSerializer(user.watchlist, many=True)
        return Response(serializer.data)
    if request.method == 'DELETE':
        user = check_auth(request)
        try:
            watchlist = Watchlist.objects.get(user=user, token=request.data['token'])
            watchlist.delete()
        except:
            pass
        serializer = WatchlistSerializer(user.watchlist, many=True)
        return Response(serializer.data)
