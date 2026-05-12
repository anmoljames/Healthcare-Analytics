# Healthcare Analytics

A hospital-operations analytics project built on **SQL + Power BI**. It models patients, doctors, departments, and 12,000 visit records across FY 2024-25, and answers operations questions: revenue mix, admission rates, length of stay, and discharge outcomes.

## Dashboard preview

<div align="center">
  <img src="./Healthcare Dashboard Preview.png" alt="Healthcare Analytics dashboard preview" />
</div>

- Full KPI summary: [`Healthcare Dashboard.pdf`](./Healthcare%20Dashboard.pdf)
- Interactive version: build the 4-page report in Power BI Desktop with [`powerbi/README.md`](./powerbi/README.md) (star schema + DAX), then Publish to web for a live link.

## Project layout
```
data/              synthetic CSVs (patients, doctors, departments, visits)
scripts/           data generator (python, seeded)
sql/01_schema.sql  MySQL schema + bulk import
sql/02_kpi_queries.sql  revenue, admissions, LOS, payment-mix queries
powerbi/README.md  star schema, DAX measures, report pages
```

## How to run
1. `pip install -r requirements.txt` (only needed to regenerate data)
2. Generate data: `python scripts/generate_data.py`
3. Create MySQL DB: run `sql/01_schema.sql`
4. Run KPIs: `sql/02_kpi_queries.sql`
5. Build the dashboard in Power BI Desktop using `powerbi/README.md`

## Data note
Synthetic data generated with a fixed seed — no real patient information. Re-run `generate_data.py` to recreate identical datasets.

## Key insights
- Admission rate by department highlights which units drive inpatient load
- Oncology and Emergency carry the highest average length of stay
- Insurance accounts for the largest revenue share, but cash/UPI is growing
