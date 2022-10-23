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
            serializer = WatchlistSerializer(watchlist_obj)
            return Response(serializer.data)
        except IntegrityError:
            return Response(data='Token already exists in user\'s watchlist', status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        user = check_auth(request)
        watchlist = Watchlist.objects.get(user=user, token=request.data['token'])
        watchlist.delete()
        return Response(status=status.HTTP_200_OK)
