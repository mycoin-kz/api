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
    cryptocompare_imageurl = models.CharField(max_length=255)
    cryptocompare_assetlaunchdate = models.CharField(max_length=255)
    cryptocompare_assetwebsiteurl = models.CharField(max_length=255)
    coin_status = models.CharField(max_length=255)


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
