import pandas as pd
import numpy as np
import yfinance as yf

def load_portfolio(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        df = df.dropna(subset=['Stock'])
        df['Avg Price'] = (
            df['Avg Price'].astype(str)
            .str.replace(r'[^\d]', '', regex=True)
            .replace('', np.nan)
            .dropna()
            .astype(float)
        )
        return df
    except:
        return pd.DataFrame()

def get_current_price(ticker):
    try:
        if not ticker.endswith('.JK'):
            ticker += '.JK'
        data = yf.Ticker(ticker).history(period='1d')
        return data['Close'].iloc[-1] if not data.empty else np.nan
    except:
        return np.nan
