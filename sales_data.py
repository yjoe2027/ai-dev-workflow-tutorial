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
