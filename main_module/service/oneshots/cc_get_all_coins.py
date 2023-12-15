import time
import requests
import pandas as pd
import warnings
# from ..internal_tools.sqlfunctions import execute_many

if __name__ == '__main__':
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
    print(tuples, list(allcoinslist_df.columns))
    # execute_many(None, allcoinslist_df, "public.tokenslist")

    # conn.close()

    del allcoinslist_df
    # print("--- Insert DataFrame: %s seconds ---" % (time.time() - start_time))
