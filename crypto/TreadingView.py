from tradingview_ta import TA_Handler, Interval

def get_gold_price():
    symbol = "XAUUSD"
    exchange = "OANDA"

    handler = TA_Handler()
    handler.set_symbol_as(symbol)
    handler.set_exchange(exchange)
    handler.set_screener_as_forex()
    handler.set_interval_as(Interval.INTERVAL_1_MINUTE)  # You can change the interval as needed

    analysis = handler.get_analysis()
    if analysis is not None and "error" not in analysis:
        gold_price = analysis.summary.get("summary", {}).get("last", None)
        if gold_price is not None:
            return f"The current price of gold (XAUUSD) is {gold_price}"
        else:
            return "Failed to retrieve gold price. Please try again later."
    else:
        return "Failed to retrieve gold price. Please try again later."

# Example usage:
print(get_gold_price())
