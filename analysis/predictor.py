from prophet import Prophet
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

def prophet_forecast(ticker):
    if not ticker.endswith('.JK'):
        ticker += '.JK'
    df = yf.Ticker(ticker).history(period="1y")[['Close']].reset_index()
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)  # ✅ Hapus timezone
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Prediksi'))
    fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name='Aktual'))
    fig.update_layout(
        title=f"Prediksi Harga Saham {ticker}",
        xaxis_title="Tanggal",
        yaxis_title="Harga"
    )
    return forecast, fig
