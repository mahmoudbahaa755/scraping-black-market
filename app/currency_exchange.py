import requests

def get_exchange_rate(from_currency, to_currency, amount):
	url = "https://currency-exchange.p.rapidapi.com/exchange"

	querystring = {"from": from_currency, "to": to_currency, "q": str(amount)}

	headers = {
		"X-RapidAPI-Key": "3b71192950mshe25f3516b547b97p194e63jsn3ec1092ab37a",
		"X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)

	return response.json()

# Usage
print(get_exchange_rate("SGD", "MYR", 1.0))