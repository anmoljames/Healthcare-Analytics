"""Healthcare Analytics — interactive Streamlit dashboard (free hosting alternative to Power BI).

Run locally:  streamlit run streamlit_app.py
Deploy free:  https://share.streamlit.io -> New app -> repo Healthcare-Analytics, file streamlit_app.py
Data: synthetic CSVs in data/ (no real patient information).
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Healthcare Analytics Dashboard", layout="wide")
st.title("🏥 Healthcare Analytics Dashboard")
st.caption("Hospital operations on 12,000 synthetic visits · SQL + Python + Power BI project")


@st.cache_data
def load_data():
    visits = pd.read_csv(ROOT / "data" / "visits.csv", parse_dates=["visit_date"])
    departments = pd.read_csv(ROOT / "data" / "departments.csv")
    doctors = pd.read_csv(ROOT / "data" / "doctors.csv")
    visits["year_month"] = visits["visit_date"].dt.strftime("%Y-%m")
    return visits, departments, doctors


visits_all, departments, doctors = load_data()

with st.sidebar:
    st.header("Filters")
    dept_options = sorted(visits_all.merge(departments, on="department_id")["department_name"].unique())
    sel_depts = st.multiselect("Department", dept_options, default=dept_options)
    pay_options = sorted(visits_all["payment_method"].unique())
    sel_pay = st.multiselect("Payment method", pay_options, default=pay_options)

visits = visits_all[
    visits_all.merge(departments, on="department_id")["department_name"].isin(sel_depts)
    & visits_all["payment_method"].isin(sel_pay)
].copy()
admitted = visits[visits["admitted_flag"] == 1]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total visits", f"{len(visits):,}")
c2.metric("Total revenue", f"₹{visits['treatment_cost_inr'].sum() / 1e7:.1f} Cr")
c3.metric("Admission rate", f"{len(admitted) / max(len(visits), 1) * 100:.1f}%")
c4.metric("Avg stay (admitted)", f"{admitted['length_of_stay_days'].mean():.1f} days")
c5.metric("Avg cost / visit", f"₹{visits['treatment_cost_inr'].mean():,.0f}")

tab1, tab2, tab3 = st.tabs(["Revenue", "Operations", "Doctors & Patients"])

with tab1:
    rev_month = visits.groupby("year_month")["treatment_cost_inr"].sum().reset_index()
    st.plotly_chart(px.line(rev_month, x="year_month", y="treatment_cost_inr",
                            title="Monthly revenue (INR)", markers=True), width="stretch")
    rev_dept = (visits.merge(departments, on="department_id")
                .groupby("department_name")["treatment_cost_inr"].sum()
                .sort_values(ascending=False).reset_index())
    st.plotly_chart(px.bar(rev_dept, x="department_name", y="treatment_cost_inr",
                           title="Revenue by department (INR)"), width="stretch")
    paymix = visits.groupby("payment_method")["treatment_cost_inr"].sum().reset_index()
    st.plotly_chart(px.pie(paymix, names="payment_method", values="treatment_cost_inr",
                           title="Revenue share by payment method", hole=0.4), width="stretch")

with tab2:
    los_diag = (admitted.groupby("diagnosis")["length_of_stay_days"].mean()
                .sort_values(ascending=False).head(8).reset_index())
    st.plotly_chart(px.bar(los_diag, x="length_of_stay_days", y="diagnosis", orientation="h",
                           title="Avg length of stay by diagnosis (days)"), width="stretch")
    discharge = visits["discharge_status"].value_counts().reset_index()
    discharge.columns = ["status", "count"]
    st.plotly_chart(px.pie(discharge, names="status", values="count",
                           title="Discharge outcomes", hole=0.4), width="stretch")

with tab3:
    top_docs = (visits.merge(doctors, on="doctor_id")
                .groupby(["doctor_name", "specialization"])["treatment_cost_inr"]
                .sum().sort_values(ascending=False).head(10).reset_index())
    st.subheader("Top doctors by revenue (INR)")
    st.dataframe(top_docs, width="stretch")
    st.plotly_chart(px.bar(visits.merge(doctors, on="doctor_id"), x="specialization",
                           title="Visits by specialization"), width="stretch")

st.divider()
st.caption("Synthetic data generated with a fixed seed (`scripts/generate_data.py`) — no real patient information.")
