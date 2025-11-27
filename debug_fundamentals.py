import yfinance as yf
import json

def check_fundamentals(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    fields = {
        "currentPrice": info.get("currentPrice"),
        "open": info.get("open"),
        "dayHigh": info.get("dayHigh"),
        "dayLow": info.get("dayLow"),
        "volume": info.get("volume"),
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "priceToBook": info.get("priceToBook"),
        "dividendYield": info.get("dividendYield")
    }
    
    print(json.dumps(fields, indent=4))

if __name__ == "__main__":
    check_fundamentals("RELIANCE.NS")
