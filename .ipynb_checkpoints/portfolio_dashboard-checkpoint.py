import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App Config
st.set_page_config(page_title="SafeSpace Risk Dashboard", layout="wide")

# 🌙/🌞 Theme Toggle at the Top
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "Light"

with st.container():
    col1, col2 = st.columns([6, 1])  # Spacer and small button
    with col2:
        theme_button = st.button(
            f"🌞" if st.session_state["theme_mode"] == "Dark" else "🌙",
            key="theme_toggle_button",
            help="Toggle Light/Dark Theme",
        )
        if theme_button:
            st.session_state["theme_mode"] = (
                "Light" if st.session_state["theme_mode"] == "Dark" else "Dark"
            )

theme = st.session_state["theme_mode"]

# Apply simple dark/light background
if theme == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #111;
            color: #eee;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: #fff;
            color: #000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Tabs instead of Sidebar
tab = st.tabs(["Investment Simulator", "Loan Risk Assessment", "Investment Risk Assessment"])

# ---------- DATA LOADING ----------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(
            r"../dummy_stock_prediction_data_50yrs.csv"
        )
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception:
        # Mock 10 tickers if file not found
        dates = pd.date_range(start="1975-01-01", end="2025-01-01", freq='M')
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'DIS']
        data = []
        for ticker in tickers:
            prices = np.cumprod(1 + np.random.normal(0.01, 0.05, len(dates))) * 100
            df_temp = pd.DataFrame({'date': dates, 'ticker': ticker, 'close_price': prices})
            data.append(df_temp)
        df = pd.concat(data)
        return df

# Reload Button
if st.sidebar.button("🔄 Reload Real Data", key="reload_button"):
    load_data.clear()

# ---------- PAGES ----------
def portfolio_simulator():
    st.title("📊 Investment Simulator")

    df = load_data()

    amount = st.number_input("💵 Total Investment Amount (USD)", value=10000)
    selected_tickers = st.multiselect("Select Stocks", options=df['ticker'].unique(), default=['AAPL', 'MSFT', 'GOOGL'])
    date_range = st.date_input("Select Date Range", [df['date'].min().date(), df['date'].max().date()])

    allocations = {}
    for ticker in selected_tickers:
        allocations[ticker] = st.slider(f"{ticker} Allocation %", 0, 100, 100 // len(selected_tickers), key=f"alloc_{ticker}")

    total_alloc = sum(allocations.values())
    if total_alloc != 100:
        st.error("Allocations must total 100%.")
        return

    portfolio_returns = []
    weighted_returns = []
    col1, col2 = st.columns(2)

    for ticker in selected_tickers:
        data = df[(df['ticker'] == ticker) & (df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))]

        if len(data) >= 2:
            data = data.sort_values('date')
            data['return'] = data['close_price'].pct_change()
            data.dropna(inplace=True)

            initial = data.iloc[0]['close_price']
            final = data.iloc[-1]['close_price']
            percent_change = (final - initial) / initial
            investment = amount * allocations[ticker] / 100
            result_amount = investment * (1 + percent_change)

            std_dev = np.std(data['return']) if not data['return'].empty else 0
            sharpe_ratio = (data['return'].mean() / std_dev) * np.sqrt(252) if std_dev != 0 else 0
            max_drawdown = ((data['close_price'].cummax() - data['close_price']) / data['close_price'].cummax()).max()

            weighted_returns.append(data['return'] * (allocations[ticker] / 100))

            with col1:
                st.subheader(f"📈 {ticker} Summary")
                st.write(f"**Start Price:** ${initial:.2f}")
                st.write(f"**End Price:** ${final:.2f}")
                st.markdown(f"""
                - **Initial Investment:** ${investment:,.2f}  
                - **Final Value:** ${result_amount:,.2f}  
                - **Return:** {"+" if percent_change >= 0 else ""}{percent_change*100:.2f}%
                """)
                st.write(f"**Volatility (Std Dev):** {std_dev:.4f}")
                st.write(f"**Sharpe Ratio:** {sharpe_ratio:.2f}")
                st.write(f"**Max Drawdown:** {max_drawdown:.2%}")

            with col2:
                st.line_chart(data.set_index('date')['close_price'])

            portfolio_returns.append(result_amount)

        else:
            st.warning(f"Not enough data for {ticker}.")

    # Portfolio Summary
    if portfolio_returns:
        total_return = sum(portfolio_returns)
        combined_returns = sum(weighted_returns)
        portfolio_std = np.std(combined_returns)
        portfolio_mean = np.mean(combined_returns)
        portfolio_sharpe = portfolio_mean / portfolio_std * np.sqrt(252) if portfolio_std != 0 else 0

        st.markdown("---")
        st.header("💼 Portfolio Summary")

        total_percent_change = ((total_return - amount) / amount) * 100
        if total_percent_change >= 0:
            st.success(f"🎉 Positive Return! Your investment grew by **{total_percent_change:.2f}%**!")
        else:
            st.error(f"⚠️ Negative Return! Your investment shrunk by **{total_percent_change:.2f}%**.")

        st.write(f"**Initial Investment:** ${amount:,.2f}")
        st.write(f"**Final Value:** ${total_return:,.2f}")
        st.write(f"**Portfolio Volatility:** {portfolio_std:.4f}")
        st.write(f"**Portfolio Sharpe Ratio:** {portfolio_sharpe:.2f}")

        st.line_chart(combined_returns.cumsum())

def loan_risk_assessment():
    st.title("🏦 Loan Risk Assessment")

    loan_amount = st.number_input("Loan Amount (USD)", min_value=1000, value=5000, step=500)
    loan_term = st.slider("Loan Term (Years)", 1, 30, 10)
    interest_rate = st.slider("Interest Rate (%)", 0.0, 15.0, 5.0)
    credit_score = st.slider("Credit Score", 300, 850, 700)
    annual_income = st.number_input("Annual Income (USD)", min_value=0, value=50000, step=1000)
    monthly_debt = st.number_input("Monthly Debt Payments (USD)", min_value=0, value=500, step=50)

    def predict_loan_risk(credit_score, debt_to_income_ratio):
        if credit_score < 580 or debt_to_income_ratio > 0.5:
            return "High Risk"
        elif 580 <= credit_score <= 700 or 0.3 <= debt_to_income_ratio <= 0.5:
            return "Medium Risk"
        else:
            return "Low Risk"

    debt_to_income_ratio = (monthly_debt * 12) / (annual_income + 1e-9)
    loan_risk = predict_loan_risk(credit_score, debt_to_income_ratio)

    st.write(f"Loan Amount: ${loan_amount:,.2f}")
    st.write(f"Loan Term: {loan_term} years @ {interest_rate:.2f}%")
    st.write(f"Debt-to-Income Ratio: {debt_to_income_ratio:.2f}")
    st.write(f"Credit Score: {credit_score}")
    st.subheader(f"🔮 Predicted Loan Risk: **{loan_risk}**")

def investment_risk_assessment():
    st.title("💰 Investment Risk Assessment (Bank Data)")

    mock_plaid_data = {
        "avg_monthly_income": 5000,
        "avg_monthly_expenses": 4000,
        "emergency_fund_balance": 12000,
        "monthly_debt_payments": 800,
        "avg_balance_fluctuation": 0.15,
    }

    def assess_investment_risk(data):
        savings_rate = (data["avg_monthly_income"] - data["avg_monthly_expenses"]) / (data["avg_monthly_income"] + 1e-9)
        debt_to_income = data["monthly_debt_payments"] / (data["avg_monthly_income"] + 1e-9)

        if savings_rate > 0.2 and debt_to_income < 0.3 and data["avg_balance_fluctuation"] < 0.2:
            return "Aggressive (High Risk Tolerance)"
        elif savings_rate > 0.1 and debt_to_income < 0.4:
            return "Moderate Risk Tolerance"
        else:
            return "Conservative (Low Risk Tolerance)"

    investment_risk_profile = assess_investment_risk(mock_plaid_data)

    st.subheader(f"🔮 Predicted Investment Risk Profile: **{investment_risk_profile}**")
    st.write(f"Average Monthly Income: ${mock_plaid_data['avg_monthly_income']:,.2f}")
    st.write(f"Average Monthly Expenses: ${mock_plaid_data['avg_monthly_expenses']:,.2f}")
    st.write(f"Emergency Fund Balance: ${mock_plaid_data['emergency_fund_balance']:,.2f}")
    st.write(f"Debt-to-Income Ratio: {mock_plaid_data['monthly_debt_payments'] / mock_plaid_data['avg_monthly_income']:.2f}")
    st.write(f"Cashflow Volatility: {mock_plaid_data['avg_balance_fluctuation']*100:.2f}%")

# ---------- Page Logic ----------
with tab[0]:
    portfolio_simulator()

with tab[1]:
    loan_risk_assessment()

with tab[2]:
    investment_risk_assessment()
