import time
import requests
import pandas as pd
import warnings
from random import randint

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()
from main_module.models import Token, TwitterData, FacebookData, RedditData, CodrepoData, TechIndicators

# from ..internal_tools.sqlfunctions import execute_many

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    start_time = time.time()

    URL_ALL_COINS = "https://min-api.cryptocompare.com/data/all/coinlist"
    coins_json = requests.get(URL_ALL_COINS).json()

    allcoinslist_df = pd.DataFrame(
        columns=[
            "Id",
            "Symbol",
            "CoinName",
            "FullName",
            "ImageUrl",
            "AssetLaunchDate",
            "AssetWebsiteUrl",
        ]
    )

    for token_key in list(coins_json["Data"].keys()):
        if (
            not coins_json["Data"][token_key]["IsTrading"]
            or not coins_json["Data"][token_key]["Rating"]["Weiss"]["Rating"]
        ):
            continue
        norm_df = pd.json_normalize(coins_json["Data"][token_key])[
            ["Id", "Symbol", "CoinName", "FullName"]
        ]

        try:
            temp_var = coins_json["Data"][token_key]["ImageUrl"]
            if temp_var == "":
                norm_df["ImageUrl"] = None
            else:
                baseurl = "https://www.cryptocompare.com"
                norm_df["ImageUrl"] = baseurl + temp_var
        except:
            norm_df["ImageUrl"] = None

        try:
            temp_var = (
                coins_json["Data"][token_key]["AssetLaunchDate"]
                .replace(" ", "")
                .replace(" ", "")
            )
            if (temp_var == "0000-00-00") | (temp_var == ""):
                norm_df["AssetLaunchDate"] = None
            else:
                norm_df["AssetLaunchDate"] = temp_var
        except:
            norm_df["AssetLaunchDate"] = None

        try:
            temp_var = coins_json["Data"][token_key]["AssetWebsiteUrl"]
            if temp_var == "":
                norm_df["AssetWebsiteUrl"] = None
            else:
                norm_df["AssetWebsiteUrl"] = temp_var
        except:
            norm_df["AssetWebsiteUrl"] = None

        # allcoinslist_df = allcoinslist_df.append(norm_df)
        allcoinslist_df = pd.concat([allcoinslist_df, norm_df])

    # print("--- Get DataFrame: %s seconds ---" % (time.time() - start_time))

    allcoinslist_df = allcoinslist_df.rename(
        columns={
            "Id": "cryptocompare_id",
            "Symbol": "cryptocompare_symbol",
            "CoinName": "cryptocompare_coinname",
            "FullName": "cryptocompare_fullname",
            "ImageUrl": "cryptocompare_imageurl",
            "AssetLaunchDate": "cryptocompare_assetlaunchdate",
            "AssetWebsiteUrl": "cryptocompare_assetwebsiteurl",
        }
    )

    allcoinslist_df["coingecko_id"] = "NOT_PARSED"
    allcoinslist_df["coingecko_symbol"] = "NOT_PARSED"
    allcoinslist_df["coingecko_name"] = "NOT_PARSED"
    allcoinslist_df["coin_status"] = 0

    allcoinslist_df = allcoinslist_df[
        [
            "cryptocompare_id",
            "cryptocompare_symbol",
            "cryptocompare_coinname",
            "cryptocompare_fullname",
            "coingecko_id",
            "coingecko_symbol",
            "coingecko_name",
            "cryptocompare_imageurl",
            "cryptocompare_assetlaunchdate",
            "cryptocompare_assetwebsiteurl",
            "coin_status",
        ]
    ]

    # print("--- Transform DataFrame: %s seconds ---" % (time.time() - start_time))

    # Inserting all df
    # conn = connect(param_dic)
    tuples = [tuple(x) for x in allcoinslist_df.to_numpy()]

    print(len(tuples), len(coins_json["Data"]))
    for t in tuples:
        token, _ = Token.objects.get_or_create(cryptocompare_id=t[0])
        # token.cryptocompare_id = t[0]
        token.cryptocompare_symbol = t[1]
        token.cryptocompare_coinname = t[2]
        token.cryptocompare_fullname = t[3]
        token.coingecko_id = t[4]
        token.coingecko_symbol = t[5]
        token.coingecko_name = t[6]
        token.cryptocompare_imageurl = t[7]
        token.cryptocompare_assetlaunchdate = t[8]
        token.cryptocompare_assetwebsiteurl = t[9]
        token.coin_status = t[10]

        token.imageurl = token.cryptocompare_imageurl
        token.fullname = token.cryptocompare_fullname
        token.symbol = token.cryptocompare_symbol

        token.codrepo_perc = randint(7200, 9999)/100.0
        token.reddit_perc = randint(7200, 9999)/100.0
        token.twitter_perc = randint(7200, 9999)/100.0
        token.fb_perc = randint(7200, 9999)/100.0

        token.total_perc = (token.fb_perc + token.reddit_perc + token.codrepo_perc + token.twitter_perc)/4

        max_signals = 11
        bearish = max_signals // randint(2, 11)
        bullish = (max_signals - bearish) // randint(1, max_signals - bearish)
        neutral = max_signals - bearish - bullish

        token.bearish = bearish
        token.bullish = bullish
        token.neutral = neutral

        token.save()

        TechIndicators.objects.create(token=token)
        TwitterData.objects.create(token=token)
        FacebookData.objects.create(token=token)
        CodrepoData.objects.create(token=token)
        RedditData.objects.create(token=token)

    del allcoinslist_df
    # print("--- Insert DataFrame: %s seconds ---" % (time.time() - start_time))
