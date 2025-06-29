import pandas as pd

def run_valuation(df):
    result = []
    for _, row in df.iterrows():
        ticker = row['Ticker']
        avg = row['Avg Price']
        pbv_fair = avg * 1.2
        per_fair = avg * 1.1
        dcf_fair = avg * 1.25
        result.append({
            'Ticker': ticker,
            'PBV Fair Price': pbv_fair,
            'PER Fair Price': per_fair,
            'DCF Fair Price': dcf_fair
        })
    return pd.DataFrame(result)
