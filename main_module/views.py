from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from main_module.models import Watchlist, Token
from .serializers import WatchlistSerializer, FullDataSerializer, SummaryDataSerializer
from django.db.utils import IntegrityError
import json


@api_view(["GET"])
def index(request):
    return Response(data="index endpoint!")


@api_view(["POST", "GET", "DELETE"])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    if request.method == "GET":
        serializer = WatchlistSerializer(request.user.watchlist, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        try:
            watchlist_obj = Watchlist(user=request.user, token=request.data["token"])
            watchlist_obj.save()
        except IntegrityError:
            pass
        serializer = WatchlistSerializer(request.user.watchlist, many=True)
        return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_watchlist(request, token_id):
    try:
        watchlist = Watchlist.objects.get(user=request.user, token=token_id)
        watchlist.delete()
    except:
        pass
    serializer = WatchlistSerializer(request.user.watchlist, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def summarydata(request, token_id):
    token = Token.objects.get(cryptocompare_id=token_id)
    return Response(SummaryDataSerializer(token).data)
    # with open("main_module/mocks/summary.json") as f:
    #     return Response(json.load(f))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def signalsdata(request, token_id):
    with open("main_module/mocks/signals.json") as f:
        return Response(json.load(f))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fulldata(request, token_id):
    token = Token.objects.get(cryptocompare_id=token_id)
    return Response(FullDataSerializer(token).data)
    # with open("main_module/mocks/fulldata.json") as f:
    #     return Response(json.load(f))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def overall_tokens(request):
    tokens = Token.objects.all()
    serializer = SummaryDataSerializer(tokens, many=True)
    return Response(serializer.data)
    # with open("main_module/mocks/summary.json") as f:
    #     summary = json.load(f)
    #     return Response([summary for i in range(0, 25)])
