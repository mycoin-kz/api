from rest_framework import serializers

from main_module import models

class WatchlistSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Watchlist
    fields = ['token']


class SummaryDataSerializer(serializers.ModelSerializer):
  coinname = serializers.CharField(source='cryptocompare_coinname')
  class Meta:
    model = models.Token
    fields = [
      "codrepo_perc",
      "fb_perc",
      "reddit_perc",
      "twitter_perc",
      "imageurl",
      "fullname",
      "symbol",
      "total_perc",
      "bullish",
      "neutral",
      "bearish",
      "cryptocompare_id",
      "coinname",
    ]


class CodrepoSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.CodrepoData
    fields = '__all__'


class FacebookSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.FacebookData
    fields = '__all__'


class TwitterSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.TwitterData
    fields = '__all__'


class RedditSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.RedditData
    fields = '__all__'


class TechIndicatorsSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.TechIndicators
    fields = '__all__'


class FullDataSerializer(serializers.ModelSerializer):
  codrepo = CodrepoSerializer(source='codrepo_data')
  facebook = FacebookSerializer(source='facebook_data')
  reddit = RedditSerializer(source='reddit_data')
  # techindicators = TechIndicatorsSerializer(source='techindicators')
  twitter = TwitterSerializer(source='twitter_data')

  class Meta:
    model = models.Token
    fields = [
      'cryptocompare_id',
      'codrepo_data',
      'facebook_data',
      'reddit_data',
      'twitter_data',
      'codrepo',
      'facebook',
      'reddit',
      'techindicators',
      'twitter',
    ]




class SignalsDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Token
    fields = [
      "codrepo_perc",
      "fb_perc",
      "reddit_perc",
      "twitter_perc",
      "imageurl",
      "fullname",
      "symbol",
      "total_perc",
      "bullish",
      "neutral",
      "bearish",
      "cryptocompare_id",
      "coinname",
    ]
