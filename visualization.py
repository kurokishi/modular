import streamlit as st
import pandas as pd
import plotly.express as px

def show_dca_section(dca_df, support):
    for _, row in dca_df.iterrows():
        st.markdown(f"### {row['Stock']} ({row['Ticker']})")
        st.write(f"Harga Sekarang: Rp {row['Current Price']:,.0f}")
        st.write(f"Performa: {row['Performance (%)']:.2f}%")
        for k, v in row['DCA'].items():
            st.write(f"DCA {k} bulan: Rp {v:,.0f}" if not pd.isna(v) else f"DCA {k} bulan: -")

def show_portfolio_summary(df):
    st.dataframe(df.style.format({'Avg Price': 'Rp {:,.0f}'}))

def show_prediction_chart(ticker, forecast_df, fig):
    st.plotly_chart(fig, use_container_width=True)
