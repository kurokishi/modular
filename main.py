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
import plotly.express as px

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
            support_raw = get_support_levels(df)
            support_result = {row['Ticker']: row['Support'] for row in support_raw}

            # Tampilkan sebagai tabel
            dca_table = []
            for _, row in dca_result.iterrows():
                dca_data = row['DCA']
                support = support_result.get(row['Ticker'], np.nan)
                current_price = row['Current Price']
                saran_dca = "🟢 Ya" if current_price <= support else "🔴 Tidak"
                dca_table.append({
                    'Saham': row['Stock'],
                    'Ticker': row['Ticker'],
                    'Avg Price': row['Avg Price'],
                    'Current Price': current_price,
                    'Performance (%)': row['Performance (%)'],
                    'DCA 6 Bulan': dca_data.get(6, np.nan),
                    'DCA 12 Bulan': dca_data.get(12, np.nan),
                    'DCA 24 Bulan': dca_data.get(24, np.nan),
                    'Support (Rp)': support,
                    'Saran Waktu DCA': saran_dca
                })

            dca_df = pd.DataFrame(dca_table)
            st.dataframe(dca_df.style.format({
                'Avg Price': 'Rp {:,.0f}',
                'Current Price': 'Rp {:,.0f}',
                'DCA 6 Bulan': 'Rp {:,.0f}',
                'DCA 12 Bulan': 'Rp {:,.0f}',
                'DCA 24 Bulan': 'Rp {:,.0f}',
                'Support (Rp)': 'Rp {:,.0f}',
                'Performance (%)': '{:.2f}%'
            }))

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
                    dividen = np.random.uniform(1.5, 6.5)  # Simulasi dividen
                    support = price * (1 - np.random.uniform(0.05, 0.15))  # Simulasi support
                    temp.append({
                        'Stock': stock,
                        'Ticker': ticker,
                        'Price': price,
                        'Performance': perf,
                        'Lot Price': price * 100,
                        'Dividen (%)': dividen,
                        'Support Level': support
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
                        'Performa (%)': row['Performance'],
                        'Dividen (%)': row['Dividen (%)'],
                        'Support (Rp)': row['Support Level']
                    })

                remaining = modal - total_cost
                result_df = pd.DataFrame(results)

                st.write(f"**Total Biaya Pembelian:** Rp {total_cost:,.0f}")
                st.write(f"**Sisa Modal:** Rp {remaining:,.0f}")
                st.dataframe(result_df.style.format({
                    'Harga per Lot (Rp)': 'Rp {:,.0f}',
                    'Total Biaya (Rp)': 'Rp {:,.0f}',
                    'Performa (%)': '{:.2f}%',
                    'Dividen (%)': '{:.2f}%',
                    'Support (Rp)': 'Rp {:,.0f}'
                }))

                # Grafik alokasi modal
                fig = px.bar(
                    result_df[result_df['Jumlah Lot'] > 0],
                    x='Saham',
                    y='Total Biaya (Rp)',
                    text='Jumlah Lot',
                    title='📊 Alokasi Modal ke Saham Performa Terbaik',
                    color='Performa (%)',
                    hover_data=['Dividen (%)', 'Support (Rp)'],
                    color_continuous_scale='Blues'
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Silakan unggah file CSV portofolio terlebih dahulu.")
