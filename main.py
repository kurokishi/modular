import streamlit as st
from data_loader import load_portfolio, get_current_price
from analysis.dca import analyze_dca
from analysis.support import get_support_levels
from analysis.valuation import run_valuation
from analysis.predictor import prophet_forecast
from analysis.recommendation import get_recommendations
from visualization import show_dca_section, show_portfolio_summary, show_prediction_chart
import pandas as pd
import numpy as np

st.set_page_config(page_title="📈 Analisis Portofolio Saham", layout="wide")
st.title("📊 Dashboard Portofolio Saham Modular")

uploaded_file = st.sidebar.file_uploader("📂 Unggah file portofolio (CSV)", type="csv")
selected_menu = st.sidebar.radio("🔍 Pilih Analisis", ["Ringkasan", "DCA & Support", "Prediksi Harga", "Valuasi Saham", "Rekomendasi", "Simulasi Pembelian Lot"])
modal = st.sidebar.number_input("💰 Modal yang Dimiliki (Rp)", min_value=0, value=10000000, step=1000000)

if uploaded_file:
    df = load_portfolio(uploaded_file)
    if df.empty:
        st.warning("File tidak valid atau kosong.")
    else:
        if selected_menu == "Ringkasan":
            st.subheader("Ringkasan Portofolio")
            show_portfolio_summary(df)

        elif selected_menu == "DCA & Support":
            st.subheader("🔍 Analisis DCA & Support")
            dca_result = analyze_dca(df)
            support_result = get_support_levels(df)
            show_dca_section(dca_result, support_result)

        elif selected_menu == "Prediksi Harga":
            st.subheader("📈 Prediksi Harga (30 hari ke depan)")
            for ticker in df['Ticker']:
                forecast_df, fig = prophet_forecast(ticker)
                st.write(f"**{ticker}**")
                st.plotly_chart(fig, use_container_width=True)

        elif selected_menu == "Valuasi Saham":
            st.subheader("💡 Valuasi Saham")
            valuation = run_valuation(df)
            st.dataframe(valuation)

        elif selected_menu == "Rekomendasi":
            st.subheader("🚦 Rekomendasi")
            rekom = get_recommendations(df)
            st.dataframe(rekom)

        elif selected_menu == "Simulasi Pembelian Lot":
            st.subheader("🛒 Simulasi Pembelian Lot")
            if modal <= 0:
                st.warning("Masukkan modal yang valid.")
            else:
                temp = []
                for _, row in df.iterrows():
                    ticker = row['Ticker']
                    stock = row['Stock']
                    avg = row['Avg Price']
                    price = get_current_price(ticker)
                    if np.isnan(price):
                        continue
                    perf = (price - avg) / avg * 100
                    temp.append({
                        'Stock': stock,
                        'Ticker': ticker,
                        'Price': price,
                        'Performance': perf,
                        'Lot Price': price * 100
                    })

                perf_df = pd.DataFrame(temp)
                perf_df = perf_df.sort_values(by='Performance', ascending=False).reset_index(drop=True)

                results = []
                total_cost = 0

                for _, row in perf_df.iterrows():
                    max_lot = (modal - total_cost) // row['Lot Price']
                    cost = max_lot * row['Lot Price']
                    total_cost += cost
                    results.append({
                        'Saham': row['Stock'],
                        'Harga per Lot (Rp)': row['Lot Price'],
                        'Jumlah Lot': max_lot,
                        'Total Biaya (Rp)': cost,
                        'Performa (%)': row['Performance']
                    })

                remaining = modal - total_cost
                result_df = pd.DataFrame(results)

                st.write(f"**Total Biaya Pembelian:** Rp {total_cost:,.0f}")
                st.write(f"**Sisa Modal:** Rp {remaining:,.0f}")
                st.dataframe(result_df.style.format({
                    'Harga per Lot (Rp)': 'Rp {:,.0f}',
                    'Total Biaya (Rp)': 'Rp {:,.0f}',
                    'Performa (%)': '{:.2f}%'
                }))
else:
    st.info("Silakan unggah file CSV portofolio terlebih dahulu.")
