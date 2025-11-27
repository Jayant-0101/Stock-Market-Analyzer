import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(ticker, period="10y"):
    """
    Fetches historical stock data for a given ticker.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., "RELIANCE.NS").
        period (str): The data period to download (default: "10y").
        
    Returns:
        pd.DataFrame: DataFrame containing the stock data.
    """
    print(f"Fetching data for {ticker}...")
    try:
        # Download data
        data = yf.download(ticker, period=period, progress=False, auto_adjust=False)
        
        if data.empty:
            print(f"No data found for {ticker}.")
            return pd.DataFrame()
            
        # Ensure index is datetime
        data.index = pd.to_datetime(data.index)
        
        # Flatten MultiIndex columns if present (yfinance sometimes returns MultiIndex)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def fetch_sector_data(tickers, period="5y"):
    """
    Fetches 'Adj Close' data for multiple tickers for sector comparison.
    
    Args:
        tickers (list): List of ticker symbols.
        period (str): Data period (default: "5y").
        
    Returns:
        pd.DataFrame: DataFrame with Adj Close prices for all tickers.
    """
    print(f"Fetching sector data for {tickers}...")
    try:
        data = yf.download(tickers, period=period, progress=False, auto_adjust=False)['Adj Close']
        
        if data.empty:
            print("No sector data found.")
            return pd.DataFrame()
            
        return data
    except Exception as e:
        print(f"Error fetching sector data: {e}")
        return pd.DataFrame()

def fetch_stock_news(ticker_symbol):
    """
    Fetches news for a given ticker.
    
    Args:
        ticker_symbol (str): Stock ticker.
        
    Returns:
        list: List of news dictionaries.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        news = ticker.news
        formatted_news = []
        for item in news:
            try:
                # Handle nested structure if present
                content = item.get('content', item)
                provider = content.get('provider', {})
                
                formatted_news.append({
                    'title': content.get('title', 'No Title'),
                    'publisher': provider.get('displayName', 'Unknown'),
                    'link': content.get('clickThroughUrl', {}).get('url', '#')
                })
            except Exception:
                continue
                
        return formatted_news
    except Exception as e:
        print(f"Error fetching news for {ticker_symbol}: {e}")
        return []

def fetch_fundamentals(ticker_symbol):
    """
    Fetches fundamental data for a given ticker.
    
    Args:
        ticker_symbol (str): Stock ticker.
        
    Returns:
        dict: Dictionary containing fundamental data.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        return {
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
            "priceToBook": info.get("priceToBook"),
            "dividendYield": info.get("dividendYield"),
            "currentPrice": info.get("currentPrice"),
            "open": info.get("open"),
            "dayHigh": info.get("dayHigh"),
            "dayLow": info.get("dayLow"),
            "volume": info.get("volume"),
            "currency": info.get("currency", "INR")
        }
    except Exception as e:
        print(f"Error fetching fundamentals for {ticker_symbol}: {e}")
        return {}

def fetch_nifty50_ticker_data():
    """
    Fetches current price data for Nifty 50 companies.
    
    Returns:
        list: List of dictionaries with symbol, price, and change data.
    """
    # Nifty 50 companies (as of 2024)
    nifty50_symbols = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
        "LT.NS", "AXISBANK.NS", "BAJFINANCE.NS", "ASIANPAINT.NS", "MARUTI.NS",
        "HCLTECH.NS", "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "NESTLEIND.NS",
        "ONGC.NS", "NTPC.NS", "TATAMOTORS.NS", "WIPRO.NS", "POWERGRID.NS",
        "M&M.NS", "TECHM.NS", "ADANIPORTS.NS", "COALINDIA.NS", "BAJAJFINSV.NS",
        "DIVISLAB.NS", "TATASTEEL.NS", "CIPLA.NS", "DRREDDY.NS", "EICHERMOT.NS",
        "HINDALCO.NS", "INDUSINDBK.NS", "HDFCLIFE.NS", "SBILIFE.NS", "GRASIM.NS",
        "BPCL.NS", "HEROMOTOCO.NS", "JSWSTEEL.NS", "BRITANNIA.NS", "APOLLOHOSP.NS",
        "ADANIENT.NS", "TATACONSUM.NS", "BAJAJ-AUTO.NS", "LTIM.NS", "UPL.NS"
    ]
    
    ticker_data = []
    
    try:
        print(f"Fetching Nifty 50 ticker data...")
        # Fetch data for all symbols at once (much faster)
        data = yf.download(nifty50_symbols, period="1d", progress=False, auto_adjust=False)
        
        if data.empty:
            print("No ticker data found.")
            return []
        
        # Process each symbol
        for symbol in nifty50_symbols:
            try:
                # Get the latest row
                if len(nifty50_symbols) > 1:
                    # Multiple symbols - data has MultiIndex columns
                    close = data['Close'][symbol].iloc[-1] if symbol in data['Close'].columns else None
                    open_price = data['Open'][symbol].iloc[-1] if symbol in data['Open'].columns else None
                else:
                    # Single symbol
                    close = data['Close'].iloc[-1]
                    open_price = data['Open'].iloc[-1]
                
                if close is not None and open_price is not None:
                    change = close - open_price
                    change_pct = (change / open_price) * 100 if open_price != 0 else 0
                    
                    # Clean symbol name
                    display_symbol = symbol.replace(".NS", "")
                    
                    ticker_data.append({
                        "symbol": display_symbol,
                        "price": f"{close:.2f}",
                        "change": f"{'+' if change >= 0 else ''}{change_pct:.2f}%"
                    })
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                continue
        
        print(f"Successfully fetched data for {len(ticker_data)} companies.")
        return ticker_data
        
    except Exception as e:
        print(f"Error fetching Nifty 50 ticker data: {e}")
        # Return fallback static data
        return [
            {"symbol": "NIFTY 50", "price": "24,300", "change": "+0.5%"},
            {"symbol": "SENSEX", "price": "80,100", "change": "+0.4%"},
        ]

if __name__ == "__main__":
    # Test the function
    df = fetch_stock_data("RELIANCE.NS", period="1mo")
    print(df.head())
