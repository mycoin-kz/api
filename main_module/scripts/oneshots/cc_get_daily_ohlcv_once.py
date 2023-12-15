import requests
import pandas as pd
from internal_tools.sqlfunctions import param_dic, connect, postgresql_to_dataframe, execute_many
from internal_tools.get_data_functions import cc_transform_ohlcv_1day
from decouple import config
import warnings
warnings.filterwarnings("ignore")

#Get tokens with status=1
conn = connect(param_dic)
select_query = """
    SELECT cryptocompare_id, cryptocompare_symbol, cryptocompare_fullname FROM tokenslist WHERE coin_status = 1;
    """
column_names = ["cryptocompare_id", "cryptocompare_symbol", "cryptocompare_fullname"]
shortlist_tokens = postgresql_to_dataframe(conn, select_query, column_names)
conn.close()

ohlcv_df = pd.DataFrame(columns=['cryptocompare_id','date','currency','open','high','low','close','volumefrom','volumeto'])

URL_OHLCV_DATA = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym='
CC_CURR = 'USD'
CC_LIMIT = 400
CC_CURR_LIM = f'&tsym={CC_CURR}&limit={CC_LIMIT}'

env_api_key = config("CC_API_KEY")
if not env_api_key:
    raise Exception("CC API Key not found in env variable")
CC_API_KEY = '&api_key='+env_api_key

for index, row in shortlist_tokens.iterrows():
    ohlcv_json = requests.get(URL_OHLCV_DATA + row['cryptocompare_symbol'] + CC_CURR_LIM + CC_API_KEY).json()
    print(ohlcv_json)
    #Get OHLCV Data
    ohlcv_df = ohlcv_df.append(cc_transform_ohlcv_1day(ohlcv_json, row['cryptocompare_id'], CC_CURR, limit1=False))

print("reached line 36", ohlcv_df.values)
conn = connect(param_dic)
execute_many(conn, ohlcv_df, 'public.cryptocompare_daily_ohlcv')
conn.close()

del ohlcv_df
del shortlist_tokens