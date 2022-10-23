from rest_framework import serializers

from main_module.models import Watchlist

class WatchlistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Watchlist
    fields = ['token']
