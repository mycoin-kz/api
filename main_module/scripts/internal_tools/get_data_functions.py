import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore")


def cc_transform_social_data(json_, social_name, coin_id):

    norm_df = pd.DataFrame()

    try:
        if social_name == 'Twitter':
            norm_df = (pd.json_normalize(json_['Data'][social_name])
            [['Points', 'account_creation', 'followers', 'statuses', 'lists', 'favourites', 'following']])
            norm_df['account_creation'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                        time.localtime(float(norm_df['account_creation'][0])))

        if social_name == 'Reddit':
            norm_df = (pd.json_normalize(json_['Data'][social_name])
            [['Points', 'posts_per_hour', 'comments_per_hour', 'comments_per_day', 'active_users', 'community_creation',
              'posts_per_day', 'subscribers']])
            norm_df['community_creation'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                          time.localtime(float(norm_df['community_creation'][0])))

        if social_name == 'Facebook':
            norm_df = (pd.json_normalize(json_['Data'][social_name])[
                ['Points', 'talking_about', 'is_closed', 'likes']])

        if social_name == 'CodeRepository':
            norm_df = (pd.json_normalize(json_['Data'][social_name]['List'][0])[
                ['forks','last_update','subscribers','stars','contributors','created_at','last_push',
                 'closed_total_issues']])
            norm_df['points'] = json_['Data'][social_name]['Points']
            norm_df['last_update'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                   time.localtime(float(norm_df['last_update'][0])))
            norm_df['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime(float(norm_df['created_at'][0])))
            norm_df['last_push'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                 time.localtime(float(norm_df['last_push'][0])))

        norm_df['cryptocompare_id'] = coin_id
        norm_df = norm_df.rename(columns={'Points': 'points'})
    except:
        norm_df = pd.DataFrame()

    return norm_df


def cc_transform_trading_signals(json_, signal):

    try:
        norm_df = (pd.json_normalize(json_['Data'][signal])[['value','score','sentiment']])
        norm_df['cryptocompare_id'] = json_['Data']['id']
        norm_df['signal'] = signal
    except:
        norm_df = pd.DataFrame()

    return norm_df


def cc_transform_ohlcv_1day(json_, coin_id, currency, limit1=True):
    try:
        if limit1:
            norm_df = (pd.json_normalize(json_['Data']['Data'][0])[
                ['time','open','high','low','close','volumefrom','volumeto']])
        else:
            norm_df = (pd.json_normalize(json_['Data']['Data'][0:len(json_['Data']['Data'])-1])[
                ['time', 'open', 'high', 'low', 'close', 'volumefrom', 'volumeto']])
        norm_df['cryptocompare_id'] = coin_id
        norm_df['currency'] = currency
        norm_df = norm_df.rename(columns={'time': 'date'})
        norm_df['date'] = norm_df['date'].apply(lambda x: time.strftime('%Y-%m-%d',
                                                                        time.localtime(float(x))))
    except Exception as error:
        norm_df = pd.DataFrame()
        print(error)

    return norm_df
