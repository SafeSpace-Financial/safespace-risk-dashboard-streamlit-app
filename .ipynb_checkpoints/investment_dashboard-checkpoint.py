# investment_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load historical stock prediction data (dummy or real)
df = pd.read_csv(../dummy_stock_prediction_data_50yrs.csv)
df['date'] = pd.to_datetime(df['date'])

st.title("📈 Investment Return Simulator")

# Sidebar Inputs
amount = st.sidebar.number_input("Investment Amount (USD)", value=1000)
ticker = st.sidebar.selectbox("Select Stock", df['ticker'].unique())
start_date = st.sidebar.date_input("Start Date", value=df['date'].min().date())
end_date = st.sidebar.date_input("End Date", value=df['date'].max().date())

# Filter data
data = df[(df['ticker'] == ticker) & (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

if len(data) < 2:
    st.warning("Not enough data to compute returns.")
else:
    initial_price = data.iloc[0]['close_price']
    final_price = data.iloc[-1]['close_price']
    percent_change = (final_price - initial_price) / initial_price
    return_amount = amount * (1 + percent_change)

    # Display results
    st.subheader(f"💹 {ticker} Investment Results")
    st.write(f"Start Price: **${initial_price:.2f}**")
    st.write(f"End Price: **${final_price:.2f}**")
    st.write(f"Percent Change: **{percent_change * 100:.2f}%**")
    st.write(f"Return on ${amount:.2f}: **${return_amount:.2f}**")

    # Plot price history
    st.line_chart(data.set_index('date')['close_price'])

