# ShopSmart Sales Dashboard — Design

**Date:** 2026-09-22
**Source:** [prd/ecommerce-analytics.md](../../../prd/ecommerce-analytics.md) (Phase 1 only)
**Task board:** [TASKS.md](../../../TASKS.md)

## Goal

A single-page Streamlit dashboard that reads `data/sales-data.csv` and shows two KPI cards (Total Sales, Total Orders), a sales trend line chart, and bar charts of sales by category and by region. It must run locally with `streamlit run app.py` and deploy unchanged to Streamlit Community Cloud.

Phase 2 items (filters, auth, exports, databases, drill-down) are out of scope.

## Decisions log

This design was brainstormed in autonomous mode: each clarifying question was answered with the recommended option. They are recorded here so they can be revisited.

| # | Question | Options considered | Decision (recommended) | Why |
|---|----------|--------------------|------------------------|-----|
| 1 | Use the browser visual companion? | Yes / No | **No** | The PRD already includes a layout sketch; text is enough. |
| 2 | Trend granularity (FR-2 allows daily or monthly) | Daily / Weekly / Monthly | **Monthly** | 482 orders over 12 months is ~1.3 per day; a daily line is noise. Twelve monthly points match the PRD sketch (Jan, Feb, Mar...). |
| 3 | How is "Total Orders" counted? | Row count / Unique `order_id` | **Unique `order_id`** | Matches the meaning of an order even if an order ever spans rows. For the sample data both give 482. |
| 4 | Currency format for Total Sales | Whole dollars / Cents | **Whole dollars** (`$116,500`) | PRD FR-1 shows `$X,XXX,XXX`. Tooltips on charts show cents. |
| 5 | Bar orientation | Vertical / Horizontal | **Horizontal**, largest at top | Matches the PRD layout sketch and keeps category names readable. |
| 6 | Code structure | One `app.py` / `app.py` + calculations module / Package with several modules | **`app.py` + `sales_data.py`** | Calculations become testable with pytest without starting Streamlit; a package is overkill for this size. |
| 7 | Chart library | Plotly Express / Streamlit native charts / Altair | **Plotly Express** | PRD tech stack; gives interactive tooltips and sorted bars easily. |
| 8 | Loading performance | Reload every rerun / `st.cache_data` | **`st.cache_data`** | Standard Streamlit practice; keeps reruns fast (NFR-1). |
| 9 | Python version for `venv/` | 3.12 / 3.14 (both installed) | **3.12** | Satisfies PRD's 3.11+ and has mature wheels for pandas/pyarrow/streamlit, closest to Streamlit Cloud defaults. |
| 10 | Environment tooling | venv + requirements.txt / uv / conda / pyproject | **`venv/` + `requirements.txt`** | Project ground rule; `requirements.txt` is what Streamlit Cloud reads. |
| 11 | Branching | Feature branch / git worktree | **Work directly on `feature/sales-dashboard`** | Project ground rule: no worktree. |

## Approaches considered

1. **Single `app.py`** — fastest to write, but calculations can only be checked by running the UI. Rejected: no pytest coverage.
2. **`app.py` + `sales_data.py` (chosen)** — pure pandas functions in one module, UI in the other. Small, testable, easy to read.
3. **Package (`dashboard/data.py`, `dashboard/charts.py`, `dashboard/layout.py`)** — cleaner separation for a large app, but adds import plumbing and files a reader has to jump between. Rejected under YAGNI.

## Architecture

```
data/sales-data.csv
        │
        ▼
sales_data.py   (pandas only, no Streamlit imports)
  load_sales_data(path) -> DataFrame
  total_sales(df) -> float
  total_orders(df) -> int
  monthly_sales(df) -> DataFrame[month, total_amount]
  sales_by_category(df) -> DataFrame[category, total_amount]   (sorted desc)
  sales_by_region(df) -> DataFrame[region, total_amount]       (sorted desc)
  format_currency(value) -> str   e.g. "$116,500"
  format_count(value) -> str      e.g. "1,234"
        │
        ▼
app.py          (Streamlit + Plotly Express, no calculations)
  title → KPI row (2 st.metric in columns) → trend line chart
  → two columns: category bar chart | region bar chart
```

### `sales_data.py`

- `REQUIRED_COLUMNS` constant: `date, order_id, product, category, region, quantity, unit_price, total_amount`.
- `load_sales_data(path)`: `pd.read_csv(path, parse_dates=["date"])`; raises `ValueError` naming any missing required columns. `quantity`, `unit_price`, and `total_amount` come from pandas type inference; if any is not numeric, it raises `ValueError`.
- Aggregations use `groupby(...)["total_amount"].sum()` and return plain two-column DataFrames with a reset index, so `app.py` can pass them straight to Plotly.
- `monthly_sales` groups by `df["date"].dt.to_period("M")` and converts back to a timestamp (first of month) so Plotly draws a proper date axis.
- Sorting for category/region is descending by `total_amount`.

### `app.py`

- `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")`.
- A cached loader wraps `load_sales_data("data/sales-data.csv")` with `@st.cache_data`. The path is built relative to `app.py` so it works from any working directory and on Streamlit Cloud.
- KPI cards: `st.metric("Total Sales", format_currency(...))` and `st.metric("Total Orders", format_count(...))` in two columns.
- Trend: `px.line(..., markers=True)` with axis titles "Month" and "Sales ($)", tooltip showing month and `$` amount with cents.
- Category and region: `px.bar(..., orientation="h")`, y-axis ordered so the largest bar sits on top, one shared accent color (color is not used to encode anything), tooltips with `$` amounts.
- All charts fill the width of their column (using whichever width option the installed Streamlit version does not flag as deprecated, so no warnings appear), with clear titles and axis labels (NFR-2).

## Error handling

- Missing CSV file or missing columns: `app.py` catches the error, shows `st.error` with a plain-language message, and calls `st.stop()`. No stack trace for the end user.
- No other defensive code: the dataset is fixed and validated at load.

## Testing

- `tests/test_sales_data.py` with pytest. Written test-first (TDD) for every function in `sales_data.py`.
- Unit tests use a small hand-built DataFrame (a few rows across 2 months, 2 categories, 2 regions) so expected values are obvious.
- One integration test loads the real CSV and checks: 482 orders, total sales ≈ 116,500.21, top category Electronics, regions {North, South, East, West}.
- `app.py` is verified by starting `streamlit run app.py` headless and confirming it serves without errors (then stopping it). No UI unit tests.

## Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI |
| `sales_data.py` | Loading, validation, aggregations, formatting |
| `tests/test_sales_data.py` | pytest tests |
| `requirements.txt` | streamlit, pandas, plotly, pytest |
| `.gitignore` | already ignores `venv/`; verified per milestone |
| `README.md` | gains a short "Run the dashboard locally" section |

## Expected output (from the PRD, verified against the CSV)

| Metric | Value |
|--------|-------|
| Total Sales | $116,500 (exact: $116,500.21) |
| Total Orders | 482 |
| Category order | Electronics, Wearables, Audio, Smart Home, Accessories |
| Region order | North, West, East, South |
