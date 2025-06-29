import pandas as pd
from data_loader import get_current_price

def get_recommendations(df):
    recs = []
    for _, row in df.iterrows():
        cur = get_current_price(row['Ticker'])
        avg = row['Avg Price']
        perf = (cur - avg) / avg * 100
        if perf > 25:
            rekom = 'JUAL'
        elif perf < -10:
            rekom = 'TAMBAH'
        else:
            rekom = 'HOLD'
        recs.append({
            'Ticker': row['Ticker'],
            'Rekomendasi': rekom,
            'Performa (%)': perf
        })
    return pd.DataFrame(recs)
