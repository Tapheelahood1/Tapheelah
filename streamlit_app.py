import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# Title
st.title("Tapheela Hood Data App Assignment, on Oct 7th")

# Load the data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.write("### Input Data and Examples")
st.dataframe(df)

# Bar chart of sales by category (unaggregated - will show as lines)
st.write("### Bar chart without aggregation (lines)")
st.bar_chart(df, x="Category", y="Sales")

# Aggregated bar chart by Category
st.write("### Bar chart with aggregation (solid bars)")
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time (sales by month)
st.write("### Sales aggregated by Month")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])  # Ensure Order_Date is in datetime format
df.set_index('Order_Date', inplace=True)  # Set the Order_Date as the index

# Group by Month using the new datetime index
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)

# Line chart of sales by month
st.line_chart(sales_by_month, y="Sales")

# Section: Your Additions

# 1. Drop down for Category
st.write("### (1) Add a dropdown for Category")
categories = df["Category"].unique()
selected_category = st.selectbox("Select Category", categories)

# 2. Multi-select for Sub_Category based on selected Category
st.write("### (2) Multi-select for Sub-Category in the selected Category")
sub_categories = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_sub_categories = st.multiselect("Select Sub_Category", sub_categories)

# Filter the dataframe based on the selected sub-categories
filtered_df = df[df["Sub_Category"].isin(selected_sub_categories)]

# 3. Line chart of sales for the selected items
st.write("### (3) Line chart of sales for the selected Sub_Categories")
if not filtered_df.empty:
    sales_filtered_by_date = filtered_df.groupby(pd.Grouper(freq='M')).sum()["Sales"]
    st.line_chart(sales_filtered_by_date)
else:
    st.write("No data available for the selected Sub-Categories.")

# 4. Show metrics for total sales, total profit, and overall profit margin
st.write("### (4) Metrics: Total Sales, Total Profit, and Overall Profit Margin")
if not filtered_df.empty:
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    overall_profit_margin = (total_profit / total_sales) * 100

    # Calculate overall profit margin for all products across categories to show delta
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
    st.write("No data available for the selected Sub-Categories.")
