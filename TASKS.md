# Tasks

This board tracks all work for the ShopSmart Sales Dashboard described in [prd/ecommerce-analytics.md](prd/ecommerce-analytics.md).

## Definition of Done

A milestone is done when:

- Its acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Its changes are committed with the milestone ID in the commit message (e.g. `TASK-3: ...`)

## To Do

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the dashboard from `main` to Streamlit Community Cloud with a public URL.
- [ ] App is deployed from `main` and loads without errors
- [ ] Public shareable URL is recorded in the README

Commit:

## In Progress

### TASK-6: Testing and refinement
Verify the dashboard against the PRD acceptance criteria and polish its appearance.
- [ ] All pytest tests pass and dashboard numbers match the PRD's Expected Output
- [ ] Dashboard runs with no errors or warnings, with clear labels on every chart and metric
- [ ] README section explains how to set up and run the dashboard locally

Commit:

## Done

### TASK-1: Environment setup and project initialization
Set up a Python virtual environment, dependencies, and a minimal Streamlit app skeleton.
- [x] `requirements.txt` lists streamlit, pandas, plotly, and pytest, and installs cleanly into `venv/`
- [x] `venv/` is ignored by git
- [x] `streamlit run app.py` starts and shows the dashboard title

Commit: e1497a9
Notes: clean

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` into a pandas DataFrame through a dedicated data module.
- [x] A data module loads the CSV with `date` parsed as dates and numeric columns as numbers
- [x] Loading validates that all required columns are present
- [x] pytest tests cover loading and validation

Commit: 01c1971
Notes: clean

### TASK-3: KPI cards implementation
Show Total Sales and Total Orders at the top of the dashboard.
- [x] Total Sales is displayed as currency (`$116,500`-style formatting)
- [x] Total Orders is displayed with thousands separators (482 for the sample data)
- [x] KPI calculations are covered by pytest tests

Commit: cc988b0
Notes: clean

### TASK-4: Sales trend chart
Add an interactive line chart of sales over time.
- [x] Line chart shows monthly sales with dates on the x-axis and sales on the y-axis
- [x] Hover tooltips show exact values
- [x] Monthly aggregation is covered by pytest tests

Commit: 9bddb97
Notes: clean

### TASK-5: Category and region breakdowns
Add bar charts of sales by product category and by region, side by side.
- [x] Category chart shows all 5 categories sorted highest to lowest (Electronics first)
- [x] Region chart shows all 4 regions sorted highest to lowest
- [x] Category and region aggregations are covered by pytest tests

Commit: 6ce2ab7
Notes: clean
