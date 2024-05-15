import requests
from bs4 import BeautifulSoup

import threading

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
			if not df.empty:
				df.columns = columns
				# df['open_time'] =  pd.to_datetime(df['open_time'],unit='ms')
				return df
			else:
				print(None)


# get_asset_data(['BTCUSDT','ETHUSDT','BNBUSDT'], Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
def boost(callback, assets, interval, depth):
    thread_list = []
    for i in range(len(assets)):
        th = threading.Thread(target = callback, args = (assets[i], interval, depth))
        thread_list.append(th)
        th.start()
    for thrd in thread_list:
        thrd.join()
    return thread_list

def scrape_currency_options(url):
    data=[]
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        title = soup.find('select', id='currency')
       
        options = title.find_all('option')
        return get_dict_data(options)
       
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return -1
    
def get_dict_data(data):

    
    scraped_data=[]
    for i in data:
         key_id=i['data-id']
         value=i['value']
         scraped_data.append({key_id:value})

    return scraped_data



def scrape_gold_website(url="https://www.dollaregypt.com/gold-price/"):
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find_all('table', class_='table table-striped table-hover tablesorter mt-3')

        data = {}

        for table in title:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')

                if cells:  # Check if the row has cells
                    key = cells[0].text.strip()  # The first cell is the key
                    buy_price = cells[1].find('span', class_='rate buy h3').text.strip()
                    sell_price = cells[2].find('span', class_='rate buy h3').text.strip()
                    last_buy_price= cells[1].find('div', class_='change small').text.strip()
                    last_sell_price= cells[2].find('div', class_='change small').text.strip()
                    data[key] = {'buy_price_change': buy_price,
                                 'last_sell_price': last_sell_price,
                                 'sell_price_change': sell_price,
                                 'last_buy_price':last_buy_price}
            if data.keys():
                break

        return data

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None