"""ShopSmart Sales Dashboard.

Run with: streamlit run app.py
All calculations live in sales_data.py; this file only lays out the page.
"""

from pathlib import Path

import streamlit as st

import sales_data

DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")


@st.cache_data
def load_data():
    return sales_data.load_sales_data(DATA_PATH)


try:
    df = load_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load the sales data: {error}")
    st.stop()

# KPI cards
sales_col, orders_col = st.columns(2)
sales_col.metric("Total Sales", sales_data.format_currency(sales_data.total_sales(df)))
orders_col.metric("Total Orders", sales_data.format_count(sales_data.total_orders(df)))
