import binance.client
from binance.client import Client
import datetime as dt
import pandas as pd


client = Client(api_key = "", api_secret = "")



def get_asset_data(assets, interval, depth):
	columns = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
	for asset in assets:
			klines = client.get_historical_klines(asset, interval, depth)
			df = pd.DataFrame(klines)
			print(df.columns)
			if not df.empty:
				print('here')
				df.columns = columns
				df['Date'] =  pd.to_datetime(df['Date'],unit='ms')
				return df
			else:
				print(None)


# get_asset_data(['BTCUSDT','ETHUSDT','BNBUSDT'], Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")