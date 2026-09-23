# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two things live here side by side:

- **A tutorial** (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`, `capstone-tools.md`, `codex-companion.md`) that teaches an AI-assisted workflow: PRD → task board → Superpowers brainstorm/plan → build → deploy.
- **The project built by following it:** a Streamlit "ShopSmart Sales Dashboard" specified in `prd/ecommerce-analytics.md` (Phase 1 only; Phase 2 items like filters, auth and exports are out of scope).

## Commands

Use the project venv (Python 3.12, `venv/`, git-ignored). Dependencies come only from `requirements.txt`.

```bash
python3.12 -m venv venv && venv/bin/pip install -r requirements.txt   # setup
venv/bin/streamlit run app.py                                         # run at http://localhost:8501
venv/bin/pytest                                                       # all tests
venv/bin/pytest tests/test_sales_data.py::test_monthly_sales_totals_each_month_oldest_first -v   # one test
venv/bin/pytest -q -W default                                         # surface deprecation warnings
```

Headless smoke check (start, confirm it serves, stop):

```bash
venv/bin/streamlit run app.py --server.headless true --server.port 8599 > "$TMPDIR/streamlit.log" 2>&1 &
curl -s --retry 20 --retry-delay 1 --retry-connrefused http://localhost:8599/_stcore/health; kill $!
```

No linter or formatter is configured.

## Architecture

- `sales_data.py` holds every calculation as plain pandas functions with **no Streamlit import**: loading and validating the CSV, KPIs, monthly/category/region aggregations, and number formatting. Aggregations return two-column DataFrames (`<key>, total_amount`); category and region are sorted highest first.
- `app.py` only lays out the page. It calls `sales_data` for every number, caches loading with `@st.cache_data`, and shows `st.error` + `st.stop()` on `FileNotFoundError`/`ValueError`. `DATA_PATH` is resolved relative to `app.py` so it works from any working directory and on Streamlit Cloud.
- Tests:
  - `tests/test_sales_data.py` has unit tests on a hand-built `sample_df` fixture, plus one test that checks the real CSV against the PRD numbers.
  - `tests/test_app.py` runs the real `app.py` through Streamlit's `AppTest` and checks that there are no errors, the KPI values, and a count of 3 charts.
  - `pytest.ini` sets `pythonpath = .` so tests can `import sales_data`.
- Charts are horizontal bars with `categoryorder="total ascending"`, so the largest bar is on top. They share one `ACCENT_COLOR`, and `st.plotly_chart(..., width="stretch")` is used (`use_container_width` is deprecated in the installed Streamlit).

Expected output for `data/sales-data.csv`, which the tests pin:

| Metric | Value |
|---|---|
| Total Sales | $116,500 (exact: 116,500.21) |
| Total Orders | 482 |
| Categories, highest first | Electronics, Wearables, Audio, Smart Home, Accessories |
| Regions, highest first | North, West, East, South |
| Months | 12 (Jan–Dec 2024) |

If any of these change, something is wrong.

## Workflow conventions

- **`TASKS.md` is the task board** (To Do / In Progress / Done). Each milestone is `TASK-N` and has checkbox criteria, a `Commit:` line and a `Notes:` line.
- When a milestone is finished:
  1. Tick its criteria.
  2. Record the short hash of its last *code* commit on the `Commit:` line.
  3. Add a Notes line: what went wrong or was corrected, or `clean`.
  4. Move it to Done.
  5. Commit the board update as `TASK-N: mark done on the board`.
- Commit messages start with the milestone ID, e.g. `TASK-3: add total_sales and total_orders`.
- Design docs are in `docs/superpowers/specs/`, implementation plans in `docs/superpowers/plans/`. Plan tasks are labelled with their `TASK-N` but numbered separately.
- **Dependencies:** keep plain `venv/` + `requirements.txt`. Do not add `pyproject.toml`, `Pipfile`, `uv.lock` or conda files. Streamlit Community Cloud reads those before `requirements.txt` and the deploy breaks.
- **Git:** work on a feature branch without git worktrees. Data calculations stay in `sales_data.py`, written test-first.
- **TASK-7 (deploy to Streamlit Community Cloud)** is done by the repo owner from `main` after the feature branch is merged: main file `app.py`, then the public URL goes into `README.md`.

## Lessons

Taken from the `Notes:` lines in `TASKS.md` (TASK-1 to TASK-5 were clean; both lessons come from TASK-6 reviews):

- When a test checks a sorted result against real data, assert the whole order, not just the first item. The PRD's sorted-chart criteria are only covered when every position is checked.
- In `app.py`, define helper functions (like `sales_bar_chart`) with the other definitions above the `try:` block. Everything below should read top to bottom as the page, with no function definitions in the middle.
