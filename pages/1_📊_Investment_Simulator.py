
import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import numpy as np

st.title("📊 Investment Simulator")

token = st.session_state.get("idToken")

if not token:
    st.error("🔒 You must be signed in to use the simulator.")
    st.stop()

# ---------- UI Inputs ----------
amount = st.number_input("💵 Total Investment Amount (USD)", value=10000)

tickers = st.multiselect(
    "Select Stocks", 
    options=["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "NVDA", "JPM", "DIS"], 
    default=["AAPL", "MSFT", "GOOGL"]
)

date_range = st.date_input(
    "Select Date Range", 
    [datetime(2010, 1, 1), datetime(2024, 12, 31)]
)

allocations = {}
for ticker in tickers:
    allocations[ticker] = st.slider(
        f"{ticker} Allocation %", 
        min_value=0, 
        max_value=100, 
        value=100 // len(tickers),
        key=f"alloc_{ticker}"
    )

# Ensure allocations sum to 100
total_alloc = sum(allocations.values())
if total_alloc != 100:
    st.error("Allocations must total 100%.")
    st.stop()

# ---------- Submit Button ----------
if st.button("📤 Simulate Portfolio"):
    with st.spinner("Simulating..."):
        # Format request payload
        form_data = {
            "amount": amount,
            "tickers": tickers,
            "allocations": allocations,
            "start_date": date_range[0].isoformat(),
            "end_date": date_range[1].isoformat()
        }

        try:
            response = requests.get(
                "http://localhost:5000/simulations/simulate-portfolio",
                json=form_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                st.error(f"❌ Error {response.status_code}: {response.text}")
                st.stop()

            result = response.json()
            # st.write('FULL BACKEND RESPONSE: ', result)

            # ---------- Render Results ----------
            st.header("💼 Portfolio Summary")
            if result["percent_gain"] >= 0:
                st.success(f"🎉 Positive Return! Your investment grew by **{result["percent_gain"]:.2f}%**!")
            else:
                st.error(f"⚠️ Negative Return! Your investment shrunk by **{result["percent_gain"]:.2f}%**.")
                
            st.write(f"**Initial Investment:** ${result['initial_investment']:,.2f}")
            # st.write(f"**Final Value:** ${result['total_return']:,.2f}")
            st.write(f"**Volatility (Std Dev):** {result['portfolio_std']:.4f}")
            st.write(f"**Sharpe Ratio:** {result['portfolio_sharpe']:.2f}")

            # Chart of cumulative returns (if available)
            # if "cumulative_returns" in result:
            #     df_returns = pd.DataFrame(result["cumulative_returns"])
            #     df_returns["date"] = pd.to_datetime(df_returns["date"])
            #     st.line_chart(df_returns.set_index("date")["value"])

            # Optional: per-stock performance
            for stock in result["results"]:
                st.subheader(f"📈 {stock['ticker']} Summary")
                performance_data = {
                    "Performance Metrics": [
                        "Start Price",
                        "End Price",
                        "Initial Investment",
                        "Final Value",
                        "Portfolio Return"
                    ],
                    "Values": [
                        f"${stock["start_price"]:.2f}",
                        f"${stock["end_price"]:.2f}",
                        f"${stock["investment"]:,.2f}",
                        f"${stock["result_amount"]:,.2f}",
                        f"{stock["percent_return"]}%"
                    ]
                }
                df_performance = pd.DataFrame(performance_data)
                st.write("**📊 Performance Overview**")
                st.dataframe(df_performance.to_dict(orient="records"), use_container_width=True)

#             # Risk Table
                risk_data = {
                    "Risk Metrics": [
                        "Volatility (Std Dev)",
                        "Sharpe Ratio",
                        "Max Drawdown"
                    ],
                    "Values": [
                        f"{stock["volatility"]:.4f}",
                        f"{stock["sharpe_ratio"]:.2f}",
                        f"{stock["max_drawdown"]:.2%}"
                    ]
                }
                df_risk = pd.DataFrame(risk_data)
                st.write("**⚠️ Risk Analysis**")
                st.dataframe(df_risk.to_dict(orient="records"), use_container_width=True)                
                


        except Exception as e:
            st.error(f"Error: {e}")


# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import altair as alt
# import requests

# st.title("📊 Investment Simulator")

# # ---------- DATA LOADING ----------
# @st.cache_data
# def load_data():
#     try:
#         df = pd.read_csv(
#             r".\dummy_stock_prediction_data_50yrs.csv"
#         )
#         df['date'] = pd.to_datetime(df['date'])
#         return df
#     except Exception:
#         # Mock 10 tickers if file not found
#         dates = pd.date_range(start="1975-01-01", end="2025-01-01", freq='M')
#         tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'DIS']
#         data = []
#         for ticker in tickers:
#             prices = np.cumprod(1 + np.random.normal(0.01, 0.05, len(dates))) * 100
#             df_temp = pd.DataFrame({'date': dates, 'ticker': ticker, 'close_price': prices})
#             data.append(df_temp)
#         df = pd.concat(data)
#         return df

# # Reload Button
# if st.sidebar.button("🔄 Reload Real Data", key="reload_button"):
#     load_data.clear()

# def portfolio_simulator():
#     df = load_data()

#     amount = st.number_input("💵 Total Investment Amount (USD)", value=10000)
#     selected_tickers = st.multiselect("Select Stocks", options=df['ticker'].unique(), default=['AAPL', 'MSFT', 'GOOGL'])
#     date_range = st.date_input("Select Date Range", [df['date'].min().date(), df['date'].max().date()])

#     allocations = {}
#     for ticker in selected_tickers:
#         allocations[ticker] = st.slider(f"{ticker} Allocation %", 0, 100, 100 // len(selected_tickers), key=f"alloc_{ticker}")

#     total_alloc = sum(allocations.values())
#     if total_alloc != 100:
#         st.error("Allocations must total 100%.")
#         return

#     portfolio_returns = []
#     weighted_returns = []

#     for ticker in selected_tickers:
#         data = df[(df['ticker'] == ticker) & (df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))]

#         if len(data) >= 2:
#             data = data.sort_values('date')
#             data['return'] = data['close_price'].pct_change()
#             data.dropna(inplace=True)

#             initial = data.iloc[0]['close_price']
#             final = data.iloc[-1]['close_price']
#             percent_change = (final - initial) / initial
#             investment = amount * allocations[ticker] / 100
#             result_amount = investment * (1 + percent_change)

#             std_dev = np.std(data['return']) if not data['return'].empty else 0
#             sharpe_ratio = (data['return'].mean() / std_dev) * np.sqrt(252) if std_dev != 0 else 0
#             max_drawdown = ((data['close_price'].cummax() - data['close_price']) / data['close_price'].cummax()).max()

#             weighted_returns.append(data['return'] * (allocations[ticker] / 100))

#             st.subheader(f"📈 {ticker} Summary")

#             # Performance Table
#             performance_data = {
#                 "Performance Metrics": [
#                     "Start Price",
#                     "End Price",
#                     "Initial Investment",
#                     "Final Value",
#                     "Portfolio Return"
#                 ],
#                 "Values": [
#                     f"${initial:.2f}",
#                     f"${final:.2f}",
#                     f"${investment:,.2f}",
#                     f"${result_amount:,.2f}",
#                     f"{'+' if percent_change >= 0 else ''}{percent_change * 100:.2f}%"
#                 ]
#             }
#             df_performance = pd.DataFrame(performance_data)
#             st.write("**📊 Performance Overview**")
#             st.dataframe(df_performance.to_dict(orient="records"), use_container_width=True)
#             st.line_chart(data.set_index('date')['close_price'])

#             # Risk Table
#             risk_data = {
#                 "Risk Metrics": [
#                     "Volatility (Std Dev)",
#                     "Sharpe Ratio",
#                     "Max Drawdown"
#                 ],
#                 "Values": [
#                     f"{std_dev:.4f}",
#                     f"{sharpe_ratio:.2f}",
#                     f"{max_drawdown:.2%}"
#                 ]
#             }
#             df_risk = pd.DataFrame(risk_data)
#             st.write("**⚠️ Risk Analysis**")
#             st.dataframe(df_risk.to_dict(orient="records"), use_container_width=True)

#             portfolio_returns.append(result_amount)

#         else:
#             st.warning(f"Not enough data for {ticker}.")

#     # Portfolio Summary
#     if portfolio_returns:
#         total_return = sum(portfolio_returns)
#         combined_returns = sum(weighted_returns)
#         portfolio_std = np.std(combined_returns)
#         portfolio_mean = np.mean(combined_returns)
#         portfolio_sharpe = portfolio_mean / portfolio_std * np.sqrt(252) if portfolio_std != 0 else 0

#         st.markdown("---")
#         st.header("💼 Portfolio Summary")

#         total_percent_change = ((total_return - amount) / amount) * 100
#         if total_percent_change >= 0:
#             st.success(f"🎉 Positive Return! Your investment grew by **{total_percent_change:.2f}%**!")
#         else:
#             st.error(f"⚠️ Negative Return! Your investment shrunk by **{total_percent_change:.2f}%**.")

#         st.write(f"**Initial Investment:** ${amount:,.2f}")
#         st.write(f"**Final Value:** ${total_return:,.2f}")
#         st.write(f"**Portfolio Volatility:** {portfolio_std:.4f}")
#         st.write(f"**Portfolio Sharpe Ratio:** {portfolio_sharpe:.2f}")

#         st.line_chart(combined_returns.cumsum())

# portfolio_simulator()