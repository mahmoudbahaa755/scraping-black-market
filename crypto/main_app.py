import my_function as fn
import boost as bs


tickers = [["ETCUSDT", "ETHUSDT"], ["LTCUSDT", "XRPUSDT"], ["XEMUSDT", "PNTUSDT"]]

import concurrent.futures

def get_crypto_data():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fn.get_asset_data, ticker, "4h", "24 hours ago UTC+1") for ticker in tickers]
    
    results = [future.result() for future in futures]
    return results

result = get_crypto_data()
print(len(result))