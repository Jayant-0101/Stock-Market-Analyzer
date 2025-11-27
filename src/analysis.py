import pandas as pd
import numpy as np

def calculate_volatility(df):
    """
    Calculates daily returns and rolling volatility.
    
    Args:
        df (pd.DataFrame): Stock data with 'Adj Close'.
        
    Returns:
        pd.DataFrame: DataFrame with added 'Daily Return', 'RollingVol_30', 'RollingVol_90'.
    """
    df = df.copy()
    df['Daily Return'] = df['Adj Close'].pct_change()
    df['RollingVol_30'] = df['Daily Return'].rolling(window=30).std()
    df['RollingVol_90'] = df['Daily Return'].rolling(window=90).std()
    return df

def calculate_seasonal_trends(df):
    """
    Calculates monthly, day-of-week, and yearly average returns.
    
    Args:
        df (pd.DataFrame): Stock data with 'Daily Return'.
        
    Returns:
        dict: Dictionary containing Series for monthly, day_of_week, and yearly returns.
    """
    df = df.copy()
    df['Month'] = df.index.month
    df['Day'] = df.index.day_name()
    df['Year'] = df.index.year
    
    monthly_returns = df.groupby('Month')['Daily Return'].mean()
    day_of_week_returns = df.groupby('Day')['Daily Return'].mean()
    # Reorder days
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    day_of_week_returns = day_of_week_returns.reindex(days_order)
    
    yearly_returns = df.groupby('Year')['Daily Return'].mean()
    
    return {
        'monthly': monthly_returns,
        'day_of_week': day_of_week_returns,
        'yearly': yearly_returns
    }

def calculate_volume_analysis(df):
    """
    Calculates volume moving averages and monthly average volume.
    
    Args:
        df (pd.DataFrame): Stock data with 'Volume'.
        
    Returns:
        pd.DataFrame, pd.Series: DataFrame with 'Volume_MA20', and Series of monthly avg volume.
    """
    df = df.copy()
    df['Volume_MA20'] = df['Volume'].rolling(window=20).mean()
    
    df['Month'] = df.index.month
    monthly_volume = df.groupby('Month')['Volume'].mean()
    
    return df, monthly_volume

def calculate_sector_performance(sector_df):
    """
    Calculates cumulative returns for sector comparison.
    
    Args:
        sector_df (pd.DataFrame): DataFrame with Adj Close prices for multiple tickers.
        
    Returns:
        pd.DataFrame: Cumulative returns.
    """
    return sector_df.pct_change().cumsum()

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def predict_price(df, days=60):
    """
    Predicts the next day's closing price using Linear Regression.
    
    Args:
        df (pd.DataFrame): Stock data.
        days (int): Number of past days to use for training.
        
    Returns:
        dict: Dictionary with 'predicted_price', 'score', and 'trend'.
    """
    df = df.copy().dropna()
    if len(df) < days:
        return None
    
    # Prepare data
    df['Numbers'] = list(range(0, len(df)))
    X = df[['Numbers']].tail(days)
    y = df['Adj Close'].tail(days)
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next day
    next_day_index = [[X.iloc[-1, 0] + 1]]
    prediction = model.predict(next_day_index)[0]
    score = model.score(X, y)
    
    return {
        'predicted_price': prediction,
        'score': score,
        'current_price': y.iloc[-1]
    }

def calculate_technical_indicators(df):
    """
    Calculates technical indicators: RSI, MACD, and Moving Averages.
    
    Args:
        df (pd.DataFrame): Stock data with 'Adj Close'.
        
    Returns:
        pd.DataFrame: DataFrame with added indicator columns.
    """
    df = df.copy()
    
    # Moving Averages
    df['SMA_50'] = df['Adj Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Adj Close'].rolling(window=200).mean()
    
    # RSI (14-day)
    delta = df['Adj Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD (12, 26, 9)
    exp1 = df['Adj Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Adj Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    return df
