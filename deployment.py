from flask import Flask, request
from flask_restful import Api, Resource
import jsonify
import pandas as pd
from scrapping_functions import scrape_currency_options ,get_dict_data,scrape_gold_website,boost,get_asset_data

import requests
from bs4 import BeautifulSoup
import concurrent.futures

    
def scrape_currency_data(url="https://dollaregypt.com",options="currency"):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the relevant data on the webpage
        title = soup.find('select', id=options)
        # gold = soup.find('select', id='gold-karat')
       
        options = title.find_all('option')
        # gold_data=get_dict_data(gold)
        data=get_dict_data(options)
         
        return data
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None

app = Flask(__name__)
api = Api(app)

def get_last_row(df):
    return df.iloc[-1, :]

@app.route('/get_crypto_data', methods=['GET'])
def get_crypto_data():
    tickers = [["ETHUSDT"], [ "XRPUSDT"], [ "BTCUSDT"]]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_asset_data, ticker, "4h", "24 hours ago UTC+1") for ticker in tickers]
    
    results = [future.result() for future in futures]
    print(results[0]['high'])
    return process_results(tickers, results)
def process_results(tickers, results):
    return [{tickers[i][0]: {
        "high": results[i]['high'].iloc[-1],
        "close": results[i]['close'].iloc[-1],
        "low": results[i]['low'].iloc[-1],
        "open": results[i]['open'].iloc[-1],
        "volume": results[i]['volume'].iloc[-1],
        
    }} for i in range(len(results))]

# Use the function like this:
# processed_results = process_results(tickers, results)

@app.route('/currency_black_market', methods=['GET'])
def get_currency_data():
    url = "https://dollaregypt.com"
    i=0
    currency_data=[]
    for _ in range(3):

        currency_data = scrape_currency_options(url)
        if currency_data:
            break
        i+=1
    if currency_data:
        return currency_data
    else:
        return jsonify({'error': 'Failed to retrieve currency data'}), 500

@app.route('/gold_price', methods=['GET'])
def get_gold_data():
    url = "https://www.dollaregypt.com/gold-price/"
    i=0
    gold_data=[]
    for _ in range(3):

        gold_data = scrape_gold_website()
        if gold_data:
            break
        i+=1
    if gold_data:
        return gold_data
    else:
        return jsonify({'error': 'Failed to retrieve gold data'}), 500
class ClassificationAPI(Resource):
        def get(self):
            # data=scrape_currency_data()
            gold_data=scrape_currency_data('https://www.dollaregypt.com/gold-price/',"gold-karat")
            # print(data)
            return {'gold_data':gold_data,'status':200,'message':'success',}

      
api.add_resource(ClassificationAPI, "/get_coins_price", methods=["GET"])
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5400)
