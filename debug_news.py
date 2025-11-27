import yfinance as yf

ticker = yf.Ticker("RELIANCE.NS")
print("Fetching news...")
try:
    news = ticker.news
    if news:
        print(f"Found {len(news)} news items.")
        print(news[0])
    else:
        print("No news found.")
except Exception as e:
    print(f"Error fetching news: {e}")
