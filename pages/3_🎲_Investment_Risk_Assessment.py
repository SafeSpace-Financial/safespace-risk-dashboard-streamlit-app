import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

st.title("🎲 Investment Risk Assessment")

def investment_risk_assessment():
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
    
investment_risk_assessment()
