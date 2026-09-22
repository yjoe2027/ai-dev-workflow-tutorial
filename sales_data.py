"""Data loading and calculations for the ShopSmart sales dashboard.

Everything here is plain pandas, so it can be tested without Streamlit.
"""

import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "total_amount",
]
NUMERIC_COLUMNS = ["quantity", "unit_price", "total_amount"]


def load_sales_data(path):
    """Load the sales CSV, check its columns, and parse the date column."""
    df = pd.read_csv(path)

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Sales data is missing columns: {', '.join(missing)}")

    not_numeric = [
        column for column in NUMERIC_COLUMNS
        if not pd.api.types.is_numeric_dtype(df[column])
    ]
    if not_numeric:
        raise ValueError(f"Sales data has non-numeric values in: {', '.join(not_numeric)}")

    df["date"] = pd.to_datetime(df["date"])
    return df


def total_sales(df):
    """Sum of all revenue."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Number of distinct orders."""
    return int(df["order_id"].nunique())


def monthly_sales(df):
    """Total sales per calendar month, oldest first.

    The `month` column holds the first day of each month.
    """
    month = df["date"].dt.to_period("M").dt.to_timestamp().rename("month")
    return df.groupby(month)["total_amount"].sum().reset_index()


def _sales_by(df, column):
    """Total sales per value of `column`, highest first."""
    return (
        df.groupby(column, as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_category(df):
    """Total sales per product category, highest first."""
    return _sales_by(df, "category")


def sales_by_region(df):
    """Total sales per region, highest first."""
    return _sales_by(df, "region")


def format_currency(value):
    """Format a dollar amount with no cents, e.g. 116500.21 -> '$116,500'."""
    return f"${value:,.0f}"


def format_count(value):
    """Format a whole number with thousands separators, e.g. 1234 -> '1,234'."""
    return f"{value:,}"
