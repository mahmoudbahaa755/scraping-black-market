from fastapi import FastAPI 
from pydantic import BaseModel
from scrapping_functions import scrape_currency_options, get_dict_data, scrape_gold_website
from get_news import get_html, get_page
import requests
from bs4 import BeautifulSoup


app = FastAPI()

class Link(BaseModel):
    link: str

app.get("/get_coins_price")
def scrape_currency_data(url="https://dollaregypt.com",options="currency"):

    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the relevant data on the webpage
        title = soup.find('select', id=options)       
        options = title.find_all('option')
        data=get_dict_data(options)
         
        return data
    else:
        return None

 

def get_last_row(df):
    return df.iloc[-1, :]

# @app.get('/get_crypto_data')
# def get_crypto_data():
#     tickers = [["ETHUSDT"], [ "XRPUSDT"], [ "BTCUSDT"]]

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = [executor.submit(get_asset_data, ticker, "4h", "24 hours ago UTC+1") for ticker in tickers]
    
#     results = [future.result() for future in futures]
#     return process_results(tickers, results)

def process_results(tickers, results):
    return [{tickers[i][0]: {
        "high": results[i]['high'].iloc[-1],
        "close": results[i]['close'].iloc[-1],
        "low": results[i]['low'].iloc[-1],
        "open": results[i]['open'].iloc[-1],
        "volume": results[i]['volume'].iloc[-1],
        
    }} for i in range(len(results))]

class Article(BaseModel):
    link: str


@app.post('/get_article')
async def get_article(article: Article):
    url = "https://www.ajnet.me/"
    return get_page(url + article.link)

@app.get('/currency_black_market')
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
        return ({'error': 'Failed to retrieve currency data'}), 500

@app.get('/get_phalstine_news')
def get_phalstine_news():
    x=get_html("https://www.ajnet.me/where/arab/palestine")
    res= {
        "data":x,
        "status":200,
        "message":"success"
    }
    return (res)
@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get('/get_news')
def get_news():
    politics=get_html("https://www.ajnet.me/politics/")
    ebusiness=get_html("https://www.ajnet.me/ebusiness/")
    res= {
        "data":politics+ebusiness,
        "status":200,
        "message":"success"
    }
    return (res)


@app.get('/gold_price',
         tags=["Gold Price"],
         response_description='Get the current gold price in Egypt',
         
         )
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
        return ({'error': 'Failed to retrieve gold data'}), 500

