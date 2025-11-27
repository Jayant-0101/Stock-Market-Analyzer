import pandas as pd
from src.data_loader import fetch_stock_data, fetch_sector_data
from src.analysis import calculate_volatility, calculate_seasonal_trends, calculate_volume_analysis, calculate_sector_performance
from src.components import create_volatility_chart, create_seasonal_charts, create_volume_chart, create_sector_chart

ticker = "RELIANCE.NS"
print(f"1. Fetching data for {ticker}...")
df = fetch_stock_data(ticker)
print(f"   Data shape: {df.shape}")
if df.empty:
    print("   Data is empty!")
    exit()

print("2. Calculating volatility...")
df = calculate_volatility(df)
print("   Done.")

print("3. Calculating seasonal trends...")
trends = calculate_seasonal_trends(df)
print("   Done.")

print("4. Calculating volume analysis...")
df, monthly_vol = calculate_volume_analysis(df)
print("   Done.")

print("5. Creating charts...")
vol_fig = create_volatility_chart(df)
monthly_fig, day_fig, yearly_fig = create_seasonal_charts(trends)
vol_fig_main, monthly_vol_fig = create_volume_chart(df, monthly_vol)
print("   Done.")

print("6. Fetching sector data...")
sector_tickers = ["TCS.NS", "INFY.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS"]
sector_data = fetch_sector_data(sector_tickers)
print(f"   Sector data shape: {sector_data.shape}")

if not sector_data.empty:
    print("7. Calculating sector performance...")
    sector_perf = calculate_sector_performance(sector_data)
    print("   Done.")
    
    print("8. Creating sector chart...")
    sector_fig = create_sector_chart(sector_perf)
    print("   Done.")
else:
    print("   Sector data empty.")

print("Full flow completed successfully.")
