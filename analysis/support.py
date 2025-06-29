import yfinance as yf
import pandas as pd

def get_support_levels(df):
    results = []
    for _, row in df.iterrows():
        ticker = row['Ticker']
        if not ticker.endswith('.JK'):
            ticker += '.JK'
        hist = yf.Ticker(ticker).history(period="6mo")
        if hist.empty:
            continue
        high, low = hist['High'].max(), hist['Low'].min()
        close = hist['Close']
        support = {
            'MA50': close.rolling(50).mean().iloc[-1] if len(close) >= 50 else None,
            'MA200': close.rolling(200).mean().iloc[-1] if len(close) >= 200 else None,
            'Fib_61.8%': high - (high - low) * 0.618
        }
        results.append({'Ticker': row['Ticker'], 'Support': support})
    return results
