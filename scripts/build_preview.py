"""Build static dashboard preview (PNG + PDF) from synthetic CSVs.

Run: python scripts/build_preview.py
Outputs: Healthcare Dashboard Preview.png, Healthcare Dashboard.pdf,
         powerbi/preview/*.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PREVIEW_DIR = ROOT / "powerbi" / "preview"
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

visits = pd.read_csv(DATA / "visits.csv", parse_dates=["visit_date"])
departments = pd.read_csv(DATA / "departments.csv")
doctors = pd.read_csv(DATA / "doctors.csv")

visits["year_month"] = visits["visit_date"].dt.strftime("%Y-%m")
admitted = visits[visits["admitted_flag"] == 1]

kpis = {
    "Total visits": len(visits),
    "Total revenue (INR)": visits["treatment_cost_inr"].sum(),
    "Admission rate %": admitted.shape[0] / len(visits) * 100,
    "Avg LOS days (admitted)": admitted["length_of_stay_days"].mean(),
    "Avg treatment cost (INR)": visits["treatment_cost_inr"].mean(),
}
rev_month = visits.groupby("year_month")["treatment_cost_inr"].sum()
rev_dept = (
    visits.merge(departments, on="department_id")
    .groupby("department_name")["treatment_cost_inr"].sum()
    .sort_values(ascending=False)
)
los_diag = admitted.groupby("diagnosis")["length_of_stay_days"].mean().sort_values(ascending=False).head(8)
discharge = visits["discharge_status"].value_counts()
paymix = visits.groupby("payment_method")["treatment_cost_inr"].sum().sort_values(ascending=False)
top_docs = (
    visits.merge(doctors, on="doctor_id")
    .groupby(["doctor_name", "specialization"])["treatment_cost_inr"].sum()
    .sort_values(ascending=False).head(5)
)

plt.rcParams.update({"figure.dpi": 120, "axes.grid": True, "grid.alpha": 0.3})
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Healthcare Analytics — Dashboard Preview (synthetic FY data)", fontsize=13, fontweight="bold")

rev_month.plot(ax=axes[0, 0], marker="o", color="#1f77b4")
axes[0, 0].set_title("Monthly revenue (INR)")
axes[0, 0].tick_params(axis="x", rotation=45)

rev_dept.plot.bar(ax=axes[0, 1], color="#2ca02c")
axes[0, 1].set_title("Revenue by department (INR)")
axes[0, 1].tick_params(axis="x", rotation=30, labelsize=8)

los_diag.plot.barh(ax=axes[1, 0], color="#ff7f0e")
axes[1, 0].set_title("Avg length of stay by diagnosis (days)")

axes[1, 1].pie(
    discharge.values, labels=discharge.index, startangle=90,
    autopct=lambda p: f"{p:.0f}%" if p > 4 else "", textprops={"fontsize": 8},
)
axes[1, 1].set_title("Discharge outcomes")

fig.tight_layout()
fig.savefig(ROOT / "Healthcare Dashboard Preview.png")
for i, ax in enumerate(fig.axes):
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(PREVIEW_DIR / f"chart_{i + 1}.png", bbox_inches=extent.expanded(1.05, 1.05))
print("PNG preview saved")

with PdfPages(ROOT / "Healthcare Dashboard.pdf") as pdf:
    pdf.savefig(fig)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.axis("off")
    lines = ["KEY PERFORMANCE INDICATORS (synthetic data)", ""] + [
        f"{k}: {v:,.1f}" if isinstance(v, float) else f"{k}: {v:,}" for k, v in kpis.items()
    ]
    lines += ["", "Top departments by revenue (INR):"] + [
        f"  {d}: {v:,.0f}" for d, v in rev_dept.head(5).items()
    ]
    lines += ["", "Top doctors by revenue (INR):"] + [
        f"  {n} ({s}): {v:,.0f}" for (n, s), v in top_docs.items()
    ]
    lines += ["", "Revenue by payment method (INR):"] + [
        f"  {m}: {v:,.0f}" for m, v in paymix.items()
    ]
    ax2.text(0.02, 0.98, "\n".join(lines), va="top", ha="left", fontsize=10, family="monospace")
    pdf.savefig(fig2)
    plt.close(fig2)
print("PDF saved")
print({k: (f"{v:,.1f}" if isinstance(v, float) else f"{v:,}") for k, v in kpis.items()})
