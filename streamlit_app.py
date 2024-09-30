import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("TH Data App Assignment, on Oct 7th")

# Load the dataset
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=['Order_Date'])
st.write("### Input Data and Examples")
st.dataframe(df)

# Step (1): Dropdown for selecting Category
selected_category = st.selectbox("Select a Category", df['Category'].unique())

# Filter data for the selected category
filtered_df = df[df['Category'] == selected_category]

# Step (2): Multi-select for Sub-Category based on the selected Category
selected_subcategories = st.multiselect("Select Sub_Category", filtered_df['Sub_Category'].unique())

# Show metrics and line chart if subcategories are selected
if selected_subcategories:
    # Filter the dataframe by selected sub-categories
    filtered_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)]

    # Step (3): Line chart of sales for selected sub-categories
    plt.figure(figsize=(12, 6))
   
    for subcategory in selected_subcategories:
        subcategory_data = filtered_df[filtered_df['Sub_Category'] == subcategory]
        sales_by_date = subcategory_data.resample('M', on='Order_Date')['Sales'].sum()
        plt.plot(sales_by_date.index, sales_by_date.values, label=subcategory, marker='o')

    plt.title('Sales by Sub_Category', fontsize=16)
    plt.xlabel('Order Date', fontsize=14)
    plt.ylabel('Sales ($)', fontsize=14)
    plt.legend(title='Sub_Category', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
   
    # Show the plot in Streamlit
    st.pyplot(plt)

    # Step (4): Calculate metrics for selected items
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    # Calculate overall average profit margin for comparison
    overall_avg_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100 if df['Sales'].sum() > 0 else 0

    # Step (4): Display metrics
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=profit_margin - overall_avg_profit_margin)
else:
    st.write("Please select at least one Sub_Category to view the sales data.")

