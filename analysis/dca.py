from data_loader import get_current_price
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

def simulate_dca(ticker, months):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        if not ticker.endswith('.JK'):
            ticker += '.JK'
        hist = yf.Ticker(ticker).history(start=start_date, end=end_date)
        return hist['Close'].mean() if not hist.empty else np.nan
    except:
        return np.nan

def analyze_dca(df):
    result = []
    for _, row in df.iterrows():
        ticker = row['Ticker']
        avg_price = row['Avg Price']
        current_price = get_current_price(ticker)
        if np.isnan(current_price):
            continue
        dca_sim = {m: simulate_dca(ticker, m) for m in [6, 12, 24]}
        result.append({
            'Stock': row['Stock'],
            'Ticker': ticker,
            'Avg Price': avg_price,
            'Current Price': current_price,
            'Performance (%)': (current_price - avg_price) / avg_price * 100,
            'DCA': dca_sim
        })
    return pd.DataFrame(result)
