import yfinance as yf
import pandas as pd

print("Pandas version:", pd.__version__)
print("yfinance version:", yf.__version__)

ticker = "RELIANCE.NS"
print(f"\nDownloading {ticker}...")
data = yf.download(ticker, period="1mo", progress=False)

print("\nColumns:", data.columns)
if isinstance(data.columns, pd.MultiIndex):
    print("Levels:", data.columns.levels)
    print("Level 0:", data.columns.get_level_values(0))
    print("Level 1:", data.columns.get_level_values(1) if data.columns.nlevels > 1 else "N/A")

print("\nHead:")
print(data.head())

print("\nAttempting flattening...")
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
print("Columns after flattening:", data.columns)
print("Head after flattening:")
print(data.head())
