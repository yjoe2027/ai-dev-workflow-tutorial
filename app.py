"""ShopSmart Sales Dashboard.

Run with: streamlit run app.py
All calculations live in sales_data.py; this file only lays out the page.
"""

from pathlib import Path

import plotly.express as px
import streamlit as st

import sales_data

DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"

# One accent color for every chart: color doesn't encode anything here.
ACCENT_COLOR = "#2563eb"

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

# Sales trend
trend = px.line(
    sales_data.monthly_sales(df),
    x="month",
    y="total_amount",
    markers=True,
    title="Sales Trend Over Time",
    labels={"month": "Month", "total_amount": "Sales ($)"},
)
trend.update_traces(
    line_color=ACCENT_COLOR,
    hovertemplate="%{x|%B %Y}<br>$%{y:,.2f}<extra></extra>",
)
trend.update_yaxes(tickprefix="$", tickformat=",.0f")
st.plotly_chart(trend, width="stretch")


def sales_bar_chart(data, column, title, label):
    """Horizontal bar chart of total sales per `column`, largest bar on top."""
    chart = px.bar(
        data,
        x="total_amount",
        y=column,
        orientation="h",
        title=title,
        labels={"total_amount": "Sales ($)", column: label},
    )
    chart.update_traces(
        marker_color=ACCENT_COLOR,
        hovertemplate="%{y}<br>$%{x:,.2f}<extra></extra>",
    )
    chart.update_yaxes(categoryorder="total ascending")
    chart.update_xaxes(tickprefix="$", tickformat=",.0f")
    return chart


# Category and region breakdowns
category_col, region_col = st.columns(2)
category_col.plotly_chart(
    sales_bar_chart(sales_data.sales_by_category(df), "category", "Sales by Category", "Category"),
    width="stretch",
)
region_col.plotly_chart(
    sales_bar_chart(sales_data.sales_by_region(df), "region", "Sales by Region", "Region"),
    width="stretch",
)
