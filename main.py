
import streamlit as st
from data_loader import load_portfolio, get_current_price
from analysis.dca import analyze_dca
from analysis.support import get_support_levels
from analysis.valuation import run_valuation
from analysis.predictor import prophet_forecast
from analysis.recommendation import get_recommendations
from visualization import show_dca_section, show_portfolio_summary, show_prediction_chart

st.set_page_config(page_title="📈 Analisis Portofolio Saham", layout="wide")
st.title("📊 Dashboard Portofolio Saham Modular")

uploaded_file = st.file_uploader("Unggah file portofolio (CSV)", type="csv")

if uploaded_file:
    df = load_portfolio(uploaded_file)
    if df.empty:
        st.warning("File tidak valid atau kosong.")
    else:
        st.subheader("Ringkasan Portofolio")
        show_portfolio_summary(df)

        st.subheader("🔍 Analisis DCA & Support")
        dca_result = analyze_dca(df)
        support_result = get_support_levels(df)
        show_dca_section(dca_result, support_result)

        st.subheader("📈 Prediksi Harga (30 hari ke depan)")
        for ticker in df['Ticker']:
            forecast_df, fig = prophet_forecast(ticker)
            st.write(f"**{ticker}**")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("💡 Valuasi Saham")
        valuation = run_valuation(df)
        st.dataframe(valuation)

        st.subheader("🚦 Rekomendasi")
        rekom = get_recommendations(df)
        st.dataframe(rekom)
else:
    st.info("Silakan unggah file CSV portofolio terlebih dahulu.")
