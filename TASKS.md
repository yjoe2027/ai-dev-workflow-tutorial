# Tasks

This board tracks all work for the ShopSmart Sales Dashboard described in [prd/ecommerce-analytics.md](prd/ecommerce-analytics.md).

## Definition of Done

A milestone is done when:

- Its acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Its changes are committed with the milestone ID in the commit message (e.g. `TASK-3: ...`)

## To Do

### TASK-1: Environment setup and project initialization
Set up a Python virtual environment, dependencies, and a minimal Streamlit app skeleton.
- [ ] `requirements.txt` lists streamlit, pandas, plotly, and pytest, and installs cleanly into `venv/`
- [ ] `venv/` is ignored by git
- [ ] `streamlit run app.py` starts and shows the dashboard title

Commit:

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` into a pandas DataFrame through a dedicated data module.
- [ ] A data module loads the CSV with `date` parsed as dates and numeric columns as numbers
- [ ] Loading validates that all required columns are present
- [ ] pytest tests cover loading and validation

Commit:

### TASK-3: KPI cards implementation
Show Total Sales and Total Orders at the top of the dashboard.
- [ ] Total Sales is displayed as currency (`$116,500`-style formatting)
- [ ] Total Orders is displayed with thousands separators (482 for the sample data)
- [ ] KPI calculations are covered by pytest tests

Commit:

### TASK-4: Sales trend chart
Add an interactive line chart of sales over time.
- [ ] Line chart shows monthly sales with dates on the x-axis and sales on the y-axis
- [ ] Hover tooltips show exact values
- [ ] Monthly aggregation is covered by pytest tests

Commit:

### TASK-5: Category and region breakdowns
Add bar charts of sales by product category and by region, side by side.
- [ ] Category chart shows all 5 categories sorted highest to lowest (Electronics first)
- [ ] Region chart shows all 4 regions sorted highest to lowest
- [ ] Category and region aggregations are covered by pytest tests

Commit:

### TASK-6: Testing and refinement
Verify the dashboard against the PRD acceptance criteria and polish its appearance.
- [ ] All pytest tests pass and dashboard numbers match the PRD's Expected Output
- [ ] Dashboard runs with no errors or warnings, with clear labels on every chart and metric
- [ ] README section explains how to set up and run the dashboard locally

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the dashboard from `main` to Streamlit Community Cloud with a public URL.
- [ ] App is deployed from `main` and loads without errors
- [ ] Public shareable URL is recorded in the README

Commit:

## In Progress

## Done
