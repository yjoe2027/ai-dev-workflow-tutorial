"""Tests for sales_data.py."""

import pandas as pd
import pytest

import sales_data

HEADER = "date,order_id,product,category,region,quantity,unit_price,total_amount\n"


def write_csv(tmp_path, text):
    path = tmp_path / "sales.csv"
    path.write_text(text)
    return path


def test_load_parses_dates_and_numbers(tmp_path):
    path = write_csv(
        tmp_path,
        HEADER
        + "2024-01-15,ORD-1,Laptop,Electronics,North,2,49.99,99.98\n"
        + "2024-02-01,ORD-2,Phone Case,Accessories,South,1,10.00,10.00\n",
    )

    df = sales_data.load_sales_data(path)

    assert len(df) == 2
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df["date"].iloc[0] == pd.Timestamp("2024-01-15")
    assert df["quantity"].iloc[0] == 2
    assert df["total_amount"].iloc[0] == pytest.approx(99.98)


def test_load_rejects_missing_columns(tmp_path):
    path = write_csv(tmp_path, "date,order_id\n2024-01-15,ORD-1\n")

    with pytest.raises(ValueError, match="missing columns: product"):
        sales_data.load_sales_data(path)


def test_load_rejects_non_numeric_amounts(tmp_path):
    path = write_csv(
        tmp_path,
        HEADER + "2024-01-15,ORD-1,Laptop,Electronics,North,2,49.99,lots\n",
    )

    with pytest.raises(ValueError, match="non-numeric values in: total_amount"):
        sales_data.load_sales_data(path)


@pytest.fixture
def sample_df():
    """Four orders over two months, three categories, three regions.

    Jan: 100 + 20 = 120    Feb: 50 + 100 = 150    Total: 270
    Electronics 200, Wearables 50, Accessories 20
    North 150, East 100, South 20
    """
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-03", "2024-02-10"]),
            "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4"],
            "product": ["Laptop", "Phone Case", "Smart Watch", "Laptop"],
            "category": ["Electronics", "Accessories", "Wearables", "Electronics"],
            "region": ["North", "South", "North", "East"],
            "quantity": [1, 2, 1, 1],
            "unit_price": [100.0, 10.0, 50.0, 100.0],
            "total_amount": [100.0, 20.0, 50.0, 100.0],
        }
    )


def test_total_sales_sums_all_revenue(sample_df):
    assert sales_data.total_sales(sample_df) == pytest.approx(270.0)


def test_total_orders_counts_orders(sample_df):
    assert sales_data.total_orders(sample_df) == 4


def test_total_orders_counts_each_order_id_once(sample_df):
    repeated = pd.concat([sample_df, sample_df.iloc[[0]]])
    assert sales_data.total_orders(repeated) == 4
