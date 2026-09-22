# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 Streamlit sales dashboard from `prd/ecommerce-analytics.md`: two KPI cards, a monthly sales trend, and sales-by-category and sales-by-region bar charts.

**Architecture:** `sales_data.py` holds all loading, validation, aggregation and formatting as plain pandas functions, tested with pytest (TDD). `app.py` is a thin Streamlit + Plotly Express page that calls those functions. A small `AppTest` smoke test runs `app.py` for real inside pytest.

**Tech Stack:** Python 3.12, `venv/` + `requirements.txt`, Streamlit, pandas, Plotly Express, pytest.

**Spec:** `docs/superpowers/specs/2026-09-22-sales-dashboard-design.md`

---

## How this plan is organised

- Plan tasks are numbered **Plan Task 1, 2, 3…**. Each is labelled with the board milestone it belongs to (**TASK-1 … TASK-7** in `TASKS.md`). The two numberings are independent.
- Every commit message starts with the milestone ID, e.g. `TASK-3: add total_sales and total_orders`.
- Work happens directly on branch `feature/sales-dashboard`. No git worktree.
- Use the project venv for every command: `venv/bin/python`, `venv/bin/pytest`, `venv/bin/streamlit`. Do not use uv, conda, pyproject.toml or Pipfile.
- **Plan Task 14 (deployment, TASK-7) is executed by the project owner, from `main`, after the branch is merged.** Agents must not perform it.

### Milestone wrap-up (run at the end of every milestone TASK-1 … TASK-6)

Before starting a milestone, move its block in `TASKS.md` from **To Do** to **In Progress** (a board edit; commit it together with the milestone's first code commit or on its own as `TASK-N: start on the board`).

At the end of the milestone:

1. Confirm `venv/` is ignored: `git check-ignore venv/` prints `venv/`, and `git status --short` shows no `venv` paths.
2. Run the full test suite: `venv/bin/pytest -v` → all pass.
3. Smoke-run the real server, confirm it answers, then stop it:
   ```bash
   venv/bin/streamlit run app.py --server.headless true --server.port 8599 > "$TMPDIR/streamlit.log" 2>&1 &
   STREAMLIT_PID=$!
   curl -s --retry 20 --retry-delay 1 --retry-connrefused http://localhost:8599/_stcore/health; echo
   kill $STREAMLIT_PID
   cat "$TMPDIR/streamlit.log"
   ```
   Expected: `ok`, and the log contains no `Traceback`, `Error` or `Warning` lines (the "install the Watchdog module" tip is fine).
4. Push: `git push`.
5. Update `TASKS.md`: tick the milestone's acceptance criteria, put the short hash of the milestone's **last code commit** on its `Commit:` line, add a `Notes:` line under it (anything that went wrong or was corrected, or `clean`), move the block to **Done**, commit as `TASK-N: mark done on the board`, and `git push`.

---

## File structure

| File | Responsibility | Created in |
|------|----------------|-----------|
| `requirements.txt` | Runtime + test dependencies (Streamlit Cloud reads this) | Plan Task 1 |
| `pytest.ini` | Puts the project root on `sys.path` so tests can `import sales_data` | Plan Task 1 |
| `app.py` | Streamlit page layout only | Plan Task 2, grown in 4, 7, 9, 11 |
| `tests/test_app.py` | `AppTest` smoke test of `app.py` | Plan Task 2, grown in 7, 9, 11 |
| `sales_data.py` | Load/validate CSV, aggregations, number formatting | Plan Task 3, grown in 5, 6, 8, 10 |
| `tests/test_sales_data.py` | Unit tests + one real-CSV integration test | Plan Task 3, grown in 5, 6, 8, 10, 12 |
| `README.md` | Add "Run the dashboard locally" section | Plan Task 13 |

---

## TASK-1: Environment setup and project initialization

### Plan Task 1 — [TASK-1] Dependencies, pytest config, venv

**Files:**
- Create: `requirements.txt`
- Create: `pytest.ini`
- Check: `.gitignore` (already contains `venv/` on line 142)

- [ ] **Step 1: Move TASK-1 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Create `requirements.txt`**

```text
streamlit>=1.50
pandas>=2.2
plotly>=5.24
pytest>=8.0
```

- [ ] **Step 3: Create `pytest.ini`**

```ini
[pytest]
pythonpath = .
testpaths = tests
```

- [ ] **Step 4: Create the venv and install**

Run:
```bash
python3.12 -m venv venv
venv/bin/pip install -r requirements.txt
```
Expected: install completes; `venv/bin/streamlit version` prints a version ≥ 1.50.

- [ ] **Step 5: Confirm `venv/` is ignored**

Run: `git check-ignore venv/ && git status --short`
Expected: `venv/` printed by check-ignore; status shows only `requirements.txt`, `pytest.ini`, `TASKS.md` — nothing under `venv/`. If `venv/` is not ignored, add a line `venv/` to `.gitignore`.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt pytest.ini TASKS.md
git commit -m "TASK-1: add requirements.txt and pytest config"
```

### Plan Task 2 — [TASK-1] Minimal app with title + smoke test

**Files:**
- Create: `app.py`
- Create: `tests/test_app.py`

- [ ] **Step 1: Create `app.py`**

```python
"""ShopSmart Sales Dashboard.

Run with: streamlit run app.py
All calculations live in sales_data.py; this file only lays out the page.
"""

import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 2: Create `tests/test_app.py`**

```python
"""Smoke test: run app.py for real with Streamlit's AppTest."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).parent.parent / "app.py"


@pytest.fixture(scope="module")
def app():
    return AppTest.from_file(str(APP_PATH)).run(timeout=30)


def test_app_runs_without_errors(app):
    assert not app.exception
    assert not app.error


def test_app_shows_title(app):
    assert app.title[0].value == "ShopSmart Sales Dashboard"
```

- [ ] **Step 3: Run tests**

Run: `venv/bin/pytest -v`
Expected: 2 passed.

- [ ] **Step 4: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "TASK-1: add minimal Streamlit app with title and smoke test"
```

- [ ] **Step 5: Milestone wrap-up for TASK-1** (see "Milestone wrap-up" above).

---

## TASK-2: Data loading and basic structure

### Plan Task 3 — [TASK-2] `load_sales_data` with validation (TDD)

**Files:**
- Create: `tests/test_sales_data.py`
- Create: `sales_data.py`

- [ ] **Step 1: Move TASK-2 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Write the failing tests** — create `tests/test_sales_data.py`:

```python
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
```

- [ ] **Step 3: Run to verify they fail**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: collection error / FAIL with `ModuleNotFoundError: No module named 'sales_data'`.

- [ ] **Step 4: Write the implementation** — create `sales_data.py`:

```python
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
```

- [ ] **Step 5: Run to verify they pass**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add sales_data.py tests/test_sales_data.py TASKS.md
git commit -m "TASK-2: add load_sales_data with column and type validation"
```

### Plan Task 4 — [TASK-2] Load the data in the app

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Replace `app.py` with**

```python
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
```

- [ ] **Step 2: Run tests**

Run: `venv/bin/pytest -v`
Expected: 5 passed (the smoke test proves the real CSV loads without an error message).

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-2: load sales data in the app with caching and error message"
```

- [ ] **Step 4: Milestone wrap-up for TASK-2.**

---

## TASK-3: KPI cards implementation

### Plan Task 5 — [TASK-3] `total_sales` and `total_orders` (TDD)

**Files:**
- Modify: `tests/test_sales_data.py`
- Modify: `sales_data.py`

- [ ] **Step 1: Move TASK-3 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Write the failing tests** — append to `tests/test_sales_data.py`:

```python
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
```

- [ ] **Step 3: Run to verify they fail**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: 3 new tests FAIL with `AttributeError: module 'sales_data' has no attribute 'total_sales'` / `'total_orders'`.

- [ ] **Step 4: Implement** — append to `sales_data.py`:

```python
def total_sales(df):
    """Sum of all revenue."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Number of distinct orders."""
    return int(df["order_id"].nunique())
```

- [ ] **Step 5: Run to verify they pass**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: 6 passed.

- [ ] **Step 6: Commit**

```bash
git add sales_data.py tests/test_sales_data.py TASKS.md
git commit -m "TASK-3: add total_sales and total_orders"
```

### Plan Task 6 — [TASK-3] Number formatting (TDD)

**Files:**
- Modify: `tests/test_sales_data.py`
- Modify: `sales_data.py`

- [ ] **Step 1: Write the failing tests** — append to `tests/test_sales_data.py`:

```python
def test_format_currency_uses_dollar_sign_and_separators():
    assert sales_data.format_currency(116500.21) == "$116,500"
    assert sales_data.format_currency(1234567) == "$1,234,567"
    assert sales_data.format_currency(0) == "$0"


def test_format_count_uses_separators():
    assert sales_data.format_count(482) == "482"
    assert sales_data.format_count(1234567) == "1,234,567"
```

- [ ] **Step 2: Run to verify they fail**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: 2 new tests FAIL with `AttributeError: ... 'format_currency'` / `'format_count'`.

- [ ] **Step 3: Implement** — append to `sales_data.py`:

```python
def format_currency(value):
    """Format a dollar amount with no cents, e.g. 116500.21 -> '$116,500'."""
    return f"${value:,.0f}"


def format_count(value):
    """Format a whole number with thousands separators, e.g. 1234 -> '1,234'."""
    return f"{value:,}"
```

- [ ] **Step 4: Run to verify they pass**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: 8 passed.

- [ ] **Step 5: Commit**

```bash
git add sales_data.py tests/test_sales_data.py
git commit -m "TASK-3: add currency and count formatting"
```

### Plan Task 7 — [TASK-3] KPI cards in the app

**Files:**
- Modify: `app.py` (append after the `try/except` block)
- Modify: `tests/test_app.py`

- [ ] **Step 1: Append to `app.py`**

```python

# KPI cards
sales_col, orders_col = st.columns(2)
sales_col.metric("Total Sales", sales_data.format_currency(sales_data.total_sales(df)))
orders_col.metric("Total Orders", sales_data.format_count(sales_data.total_orders(df)))
```

- [ ] **Step 2: Append to `tests/test_app.py`**

```python
def test_app_shows_kpis_from_prd_expected_output(app):
    kpis = {metric.label: metric.value for metric in app.metric}
    assert kpis == {"Total Sales": "$116,500", "Total Orders": "482"}
```

- [ ] **Step 3: Run tests**

Run: `venv/bin/pytest -v`
Expected: 11 passed.

- [ ] **Step 4: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "TASK-3: show Total Sales and Total Orders KPI cards"
```

- [ ] **Step 5: Milestone wrap-up for TASK-3.**

---

## TASK-4: Sales trend chart

### Plan Task 8 — [TASK-4] `monthly_sales` (TDD)

**Files:**
- Modify: `tests/test_sales_data.py`
- Modify: `sales_data.py`

- [ ] **Step 1: Move TASK-4 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Write the failing test** — append to `tests/test_sales_data.py`:

```python
def test_monthly_sales_totals_each_month_oldest_first(sample_df):
    result = sales_data.monthly_sales(sample_df)

    assert list(result.columns) == ["month", "total_amount"]
    assert list(result["month"]) == [pd.Timestamp("2024-01-01"), pd.Timestamp("2024-02-01")]
    assert list(result["total_amount"]) == pytest.approx([120.0, 150.0])
```

- [ ] **Step 3: Run to verify it fails**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: FAIL with `AttributeError: ... 'monthly_sales'`.

- [ ] **Step 4: Implement** — add to `sales_data.py` (after `total_orders`):

```python
def monthly_sales(df):
    """Total sales per calendar month, oldest first.

    The `month` column holds the first day of each month.
    """
    month = df["date"].dt.to_period("M").dt.to_timestamp().rename("month")
    return df.groupby(month)["total_amount"].sum().reset_index()
```

- [ ] **Step 5: Run to verify it passes**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: 9 passed.

- [ ] **Step 6: Commit**

```bash
git add sales_data.py tests/test_sales_data.py TASKS.md
git commit -m "TASK-4: add monthly_sales aggregation"
```

### Plan Task 9 — [TASK-4] Trend line chart in the app

**Files:**
- Modify: `app.py`
- Modify: `tests/test_app.py`

- [ ] **Step 1: Edit `app.py`.** Add `import plotly.express as px` above `import streamlit as st`; add the accent color constant under `DATA_PATH`:

```python
# One accent color for every chart: color doesn't encode anything here.
ACCENT_COLOR = "#2563eb"
```

Then append at the end of the file:

```python

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
```

- [ ] **Step 2: Append to `tests/test_app.py`**

```python
def test_app_shows_charts(app):
    assert len(app.get("plotly_chart")) >= 1
```

- [ ] **Step 3: Run tests**

Run: `venv/bin/pytest -v`
Expected: 13 passed.

- [ ] **Step 4: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "TASK-4: add monthly sales trend line chart"
```

- [ ] **Step 5: Milestone wrap-up for TASK-4.**

---

## TASK-5: Category and region breakdowns

### Plan Task 10 — [TASK-5] `sales_by_category` and `sales_by_region` (TDD)

**Files:**
- Modify: `tests/test_sales_data.py`
- Modify: `sales_data.py`

- [ ] **Step 1: Move TASK-5 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Write the failing tests** — append to `tests/test_sales_data.py`:

```python
def test_sales_by_category_sorted_highest_first(sample_df):
    result = sales_data.sales_by_category(sample_df)

    assert list(result.columns) == ["category", "total_amount"]
    assert list(result["category"]) == ["Electronics", "Wearables", "Accessories"]
    assert list(result["total_amount"]) == pytest.approx([200.0, 50.0, 20.0])


def test_sales_by_region_sorted_highest_first(sample_df):
    result = sales_data.sales_by_region(sample_df)

    assert list(result.columns) == ["region", "total_amount"]
    assert list(result["region"]) == ["North", "East", "South"]
    assert list(result["total_amount"]) == pytest.approx([150.0, 100.0, 20.0])
```

- [ ] **Step 3: Run to verify they fail**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: 2 new tests FAIL with `AttributeError: ... 'sales_by_category'` / `'sales_by_region'`.

- [ ] **Step 4: Implement** — add to `sales_data.py` (after `monthly_sales`):

```python
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
```

- [ ] **Step 5: Run to verify they pass**

Run: `venv/bin/pytest tests/test_sales_data.py -v`
Expected: 11 passed.

- [ ] **Step 6: Commit**

```bash
git add sales_data.py tests/test_sales_data.py TASKS.md
git commit -m "TASK-5: add sales_by_category and sales_by_region"
```

### Plan Task 11 — [TASK-5] Category and region bar charts in the app

**Files:**
- Modify: `app.py` (append)
- Modify: `tests/test_app.py`

- [ ] **Step 1: Append to `app.py`**

```python


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
```

- [ ] **Step 2: In `tests/test_app.py`, replace `test_app_shows_charts` with**

```python
def test_app_shows_trend_category_and_region_charts(app):
    assert len(app.get("plotly_chart")) == 3
```

- [ ] **Step 3: Run tests**

Run: `venv/bin/pytest -v`
Expected: 15 passed.

- [ ] **Step 4: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "TASK-5: add sales by category and region bar charts"
```

- [ ] **Step 5: Milestone wrap-up for TASK-5.**

---

## TASK-6: Testing and refinement

### Plan Task 12 — [TASK-6] Real-data integration test against the PRD

**Files:**
- Modify: `tests/test_sales_data.py`

- [ ] **Step 1: Move TASK-6 to In Progress in `TASKS.md`.**

- [ ] **Step 2: Append to `tests/test_sales_data.py`**

```python
def test_real_csv_matches_prd_expected_output():
    from pathlib import Path

    path = Path(__file__).parent.parent / "data" / "sales-data.csv"
    df = sales_data.load_sales_data(path)

    assert sales_data.total_orders(df) == 482
    assert sales_data.total_sales(df) == pytest.approx(116500.21, abs=0.01)
    assert sales_data.sales_by_category(df)["category"].iloc[0] == "Electronics"
    assert len(sales_data.sales_by_category(df)) == 5
    assert set(sales_data.sales_by_region(df)["region"]) == {"North", "South", "East", "West"}
    assert len(sales_data.monthly_sales(df)) == 12
```

- [ ] **Step 3: Run tests**

Run: `venv/bin/pytest -v`
Expected: 16 passed. (This test is expected to pass immediately — it checks the finished functions against the real data rather than driving new code. If it fails, stop and debug with superpowers:systematic-debugging.)

- [ ] **Step 4: Commit**

```bash
git add tests/test_sales_data.py TASKS.md
git commit -m "TASK-6: add real-data test against PRD expected output"
```

### Plan Task 13 — [TASK-6] Warnings check and README

**Files:**
- Modify: `README.md` (add a section right after the "What you'll build" section, before "## The workflow")

- [ ] **Step 1: Check for warnings.** Run `venv/bin/pytest -q -W default` and read the "warnings summary" (if any), then do the smoke-run from "Milestone wrap-up" step 3. Expected: all pass; no warnings that point at `app.py` or `sales_data.py`; the server log has no `Warning`/`Traceback` lines. If Streamlit or Plotly reports a deprecation, fix the call in `app.py` and note it for the board's `Notes:` line.

- [ ] **Step 2: Add this section to `README.md`**

````markdown
## Run the dashboard locally

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py            # opens http://localhost:8501
pytest                          # run the tests
```

The dashboard reads `data/sales-data.csv`. Calculations live in `sales_data.py` (tested in `tests/`); `app.py` only lays out the page.
````

- [ ] **Step 3: Commit**

```bash
git add README.md app.py
git commit -m "TASK-6: document how to run the dashboard locally"
```

- [ ] **Step 4: Milestone wrap-up for TASK-6.**

---

## TASK-7: Deployment to Streamlit Community Cloud

### Plan Task 14 — [TASK-7] Deploy (OWNER EXECUTES — from `main`, after the merge)

**Not for agents.** The project owner does this after `feature/sales-dashboard` is merged into `main`. TASK-7 stays in **To Do** until then.

- [ ] **Step 1:** Merge `feature/sales-dashboard` into `main` on GitHub (pull request), then `git checkout main && git pull`.
- [ ] **Step 2:** Confirm `requirements.txt`, `app.py`, `sales_data.py` and `data/sales-data.csv` are on `main` on GitHub, and there is no `pyproject.toml`, `Pipfile` or `uv.lock`.
- [ ] **Step 3:** At https://share.streamlit.io create an app: repository = this repo, branch = `main`, main file path = `app.py`. Deploy.
- [ ] **Step 4:** Open the public URL and check Total Sales ≈ $116,500, Total Orders = 482, three charts, no errors.
- [ ] **Step 5:** Add the URL to `README.md`, tick TASK-7's criteria in `TASKS.md`, record the commit, move it to Done, commit as `TASK-7: ...` and push.
