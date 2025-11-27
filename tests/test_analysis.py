import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from analysis import calculate_volatility, calculate_seasonal_trends, calculate_volume_analysis

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        # Create dummy data
        dates = pd.date_range(start='2023-01-01', periods=100)
        self.df = pd.DataFrame({
            'Adj Close': np.random.rand(100) * 100,
            'Volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
        
    def test_volatility(self):
        result = calculate_volatility(self.df)
        self.assertIn('Daily Return', result.columns)
        self.assertIn('RollingVol_30', result.columns)
        self.assertIn('RollingVol_90', result.columns)
        
    def test_seasonal_trends(self):
        # Need 'Daily Return' first
        df = calculate_volatility(self.df)
        trends = calculate_seasonal_trends(df)
        self.assertIn('monthly', trends)
        self.assertIn('day_of_week', trends)
        self.assertIn('yearly', trends)
        
    def test_volume_analysis(self):
        df, monthly_vol = calculate_volume_analysis(self.df)
        self.assertIn('Volume_MA20', df.columns)
        self.assertIsInstance(monthly_vol, pd.Series)

    def test_technical_indicators(self):
        # Need 'Adj Close'
        from analysis import calculate_technical_indicators
        df = calculate_technical_indicators(self.df)
        self.assertIn('SMA_50', df.columns)
        self.assertIn('SMA_200', df.columns)
        self.assertIn('RSI', df.columns)
        self.assertIn('MACD', df.columns)
        self.assertIn('Signal_Line', df.columns)

if __name__ == '__main__':
    unittest.main()
