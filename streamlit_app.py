import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# Title
st.title("Mortgage Repayments Calculator & Sales Analysis")

# Section: Mortgage Calculator
st.write("### Input Data for Mortgage Calculation")
home_value = st.number_input("Home Value", min_value=0, value=500000)
deposit = st.number_input("Deposit", min_value=0, value=100000)
interest_rate = st.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
loan_term = st.number_input("Loan Term (in years)", min_value=1, value=30)

# Calculate the mortgage repayments
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayment metrics
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments Summary")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Section: Sales Data Analysis
st.write("### Input Data for Sales Analysis")
df = pd.read_csv("Superstore_Sales.csv", encoding="utf-16-le", on_bad_lines="skip")
st.dataframe(df)

# 1. Dropdown for Category
categories = df["Category"].unique()
selected_category = st.selectbox("Select Category", categories)

# 2. Multi-select for Sub-Category based on selected Category
sub_categories = df[df["Category"] == selected_category]["Sub-Category"].unique()
selected_sub_categories = st.multiselect("Select Sub-Category", sub_categories)

# Filter the dataframe based on selected sub-categories
filtered_df = df[df["Sub-Category"].isin(selected_sub_categories)]

# 3. Line chart of sales for the selected sub-categories
st.write("### Sales Chart")
sales_chart_df = filtered_df.groupby('Order Date')['Sales'].sum()
st.line_chart(sales_chart_df)

# 4. Display metrics for total sales, total profit, and overall profit margin
if not filtered_df.empty:
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    overall_profit_margin = (total_profit / total_sales) * 100

    # Calculate overall profit margin for all products to show delta
    overall_avg_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    delta_margin = overall_profit_margin - overall_avg_profit_margin

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    col2.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    col3.metric(
        label="Overall Profit Margin (%)", 
        value=f"{overall_profit_margin:.2f}%", 
        delta=f"{delta_margin:.2f}%"
    )
else:
    st.write("No data available for the selected sub-categories.")

