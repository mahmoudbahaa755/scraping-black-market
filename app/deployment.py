from flask import Flask, jsonify,request
from flask_restful import Api, Resource
import pandas as pd
from app.scrapping_functions import scrape_currency_options ,get_dict_data,scrape_gold_website,boost,get_asset_data
from app.get_news import get_html,get_page
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from fastapi import FastAPI ,requests
    
def scrape_currency_data(url="https://dollaregypt.com",options="currency"):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the relevant data on the webpage
        title = soup.find('select', id=options)       
        options = title.find_all('option')
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



@app.route('/get_article', methods=['POST'])
def get_article():
    link = request.get_json()
    link = link.get('link')
    url = "https://www.ajnet.me/"
    return jsonify(get_page(url+link))


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

@app.route('/get_phalstine_news',methods=['GET'])
def get_phalstine_news():
    x=get_html("https://www.ajnet.me/where/arab/palestine")
    print('---'*40)
    print(x)
    print('---'*40)
    res= {
        "data":x,
        "status":200,
        "message":"success"
    }
    return jsonify(res)

@app.route('/get_news',methods=['GET'])
def get_news():
    politics=get_html("https://www.ajnet.me/politics/")
    ebusiness=get_html("https://www.ajnet.me/ebusiness/")
    print('---'*40)
    print('---'*40)
    res= {
        "data":politics+ebusiness,
        "status":200,
        "message":"success"
    }
    return jsonify(res)


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
    app.run(debug=True, host="0.0.0.0", port=5400)
