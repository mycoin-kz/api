from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from auth_module.models import User


class Watchlist(models.Model):
    token = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="watchlist"
    )


class Token(models.Model):
    # Primary Key
    cryptocompare_id = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )

    cryptocompare_symbol = models.CharField(max_length=255)
    cryptocompare_coinname = models.CharField(max_length=255)
    cryptocompare_fullname = models.CharField(max_length=255)
    coingecko_id = models.CharField(max_length=255)
    coingecko_symbol = models.CharField(max_length=255)
    coingecko_name = models.CharField(max_length=255)
    cryptocompare_imageurl = models.CharField(max_length=255, null=True)
    cryptocompare_assetlaunchdate = models.CharField(max_length=255, null=True)
    cryptocompare_assetwebsiteurl = models.CharField(max_length=255, null=True)
    coin_status = models.CharField(max_length=255, null=True)

    codrepo_perc = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True,
        blank=True,
    )
    fb_perc = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True,
        blank=True,
    )
    reddit_perc = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True,
        blank=True,
    )
    twitter_perc = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True,
        blank=True,
    )
    imageurl = models.CharField(max_length=512, null=True, blank=True)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    symbol = models.CharField(max_length=128, null=True, blank=True)
    total_perc = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True,
        blank=True,
    )
    bullish = models.IntegerField(null=True, blank=True)
    neutral = models.IntegerField(null=True, blank=True)
    bearish = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.cryptocompare_fullname


class TokenOHLCV(models.Model):
    token = models.OneToOneField(to=Token, on_delete=models.SET_NULL, null=True)
    date = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    open_value = models.CharField(max_length=255)
    high = models.CharField(max_length=255)
    low = models.CharField(max_length=255)
    close_value = models.CharField(max_length=255)
    volumefrom = models.CharField(max_length=255)
    volumeto = models.CharField(max_length=255)


class TwitterData(models.Model):
    token = models.OneToOneField(to=Token, on_delete=models.CASCADE, related_name='twitter_data')
    account_creation = models.IntegerField(null=True, default=1313643968000)
    favourites = models.IntegerField(null=True, default=1000)
    followers = models.IntegerField(null=True, default=844049)
    following = models.IntegerField(null=True, default=165)
    lists = models.IntegerField(null=True, default=6631)
    points = models.IntegerField(null=True, default=91055)
    statuses = models.IntegerField(null=True, default=2031)


class RedditData(models.Model):
    token = models.OneToOneField(to=Token, on_delete=models.CASCADE, related_name='reddit_data')
    active_users = models.IntegerField(null=True, default=11157)
    comments_per_day = models.FloatField(null=True, default=3368.42)
    comments_per_hour = models.FloatField(null=True, default=140.35)
    community_creation = models.IntegerField(null=True, default=1284042626000)
    points = models.IntegerField(null=True, default=4449500)
    posts_per_day = models.FloatField(null=True, default=87.36)
    posts_per_hour = models.FloatField(null=True, default=3.64)
    subscribers = models.IntegerField(null=True, default=4409293)


class FacebookData(models.Model):
    token = models.OneToOneField(to=Token, on_delete=models.CASCADE, related_name='facebook_data')
    is_closed = models.BooleanField(default=False)
    likes = models.IntegerField(null=True, default=39654)
    points = models.IntegerField(null=True, default=39654)
    talking_about = models.IntegerField(null=True, default=26)


class CodrepoData(models.Model):
    token = models.OneToOneField(to=Token, on_delete=models.CASCADE, related_name='codrepo_data')
    closed_total_issues = models.IntegerField(null=True, default=21327)
    contributors = models.IntegerField(null=True, default=1003)
    created_at = models.IntegerField(null=True, default=1292771803000)
    forks = models.IntegerField(null=True, default=29844)
    last_push = models.IntegerField(null=True, default=1631103202000)
    last_update = models.IntegerField(null=True, default=1631100509000)
    points = models.IntegerField(null=True, default=128093)
    stars = models.IntegerField(null=True, default=56870)
    subscribers = models.IntegerField(null=True, default=3845)


class TechIndicators(models.Model):
    token = models.OneToOneField(to=Token, on_delete=models.CASCADE, related_name='techindicators')
    SENTIMENT_CHOICES = [
        ("bullish", "bullish"),
        ("bearish", "bearish"),
        ("neutral", "neutral"),
    ]
    ema10 = models.FloatField(null=True, default=21419.650556424)
    ema50 = models.FloatField(null=True, default=23477.3946873044)
    ema_sentiment = models.CharField(
        max_length=10, null=True, choices=SENTIMENT_CHOICES, default="bearish"
    )
    macd_line = models.FloatField(null=True, default=-301.3443464701)
    macd_sentiment = models.CharField(
        max_length=10, null=True, choices=SENTIMENT_CHOICES, default="bullish"
    )
    macd_signal = models.FloatField(null=True, default=-864.379150169)
    mfi14 = models.FloatField(null=True, default=76.7455530806)
    mfi14_sentiment = models.CharField(
        max_length=10, null=True, choices=SENTIMENT_CHOICES, default="bullish"
    )
    mom10 = models.FloatField(null=True, default=1817.74)
    mom10_sentiment = models.CharField(
        max_length=10, null=True, choices=SENTIMENT_CHOICES, default="bullish"
    )
    rsi10 = models.FloatField(null=True, default=69.1125657987)
    rsi10_sentiment = models.CharField(
        max_length=10, null=True, choices=SENTIMENT_CHOICES, default="neutral"
    )
    rsi50 = models.FloatField(null=True, default=43.2777984936)
    rsi50_sentiment = models.CharField(
        max_length=10, null=True, choices=SENTIMENT_CHOICES, default="neutral"
    )
    sma10 = models.FloatField(null=True, default=20957.507)
    sma50 = models.FloatField(null=True, default=23114.7386)
    sma_sentiment = models.CharField(
        max_length=10, null=True, choices=SENTIMENT_CHOICES, default="bearish"
    )
