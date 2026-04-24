# Power BI Model Guide

## Star schema
- **Fact**: `visits` (visit_id PK; FKs to patients, doctors, departments)
- **Dims**: `patients`, `doctors`, `departments`
- Import all four CSV tables (`data/*.csv`) into Power BI Desktop. Set relationships: visits.patient_id→patients.patient_id, visits.doctor_id→doctors.doctor_id, visits.department_id→departments.department_id. Mark `patients/doctors/departments` as single-direction filters toward visits.

## Power Query transforms
- visits.visit_date → Date type; treatment_cost_inr → Decimal
- patients.age → Whole number
- Add column `YearMonth = Date.ToText([visit_date], "yyyy-MM")` if a clean month axis is needed

## DAX measures (create a _Measures table)
```dax
Total Visits = COUNTROWS(visits)
Total Revenue = SUM(visits[treatment_cost_inr])
Avg Treatment Cost = AVERAGE(visits[treatment_cost_inr])
Admissions = CALCULATE(COUNTROWS(visits), visits[admitted_flag] = 1)
Admission Rate % = DIVIDE([Admissions], [Total Visits], 0)
Avg Length of Stay = AVERAGE(visits[length_of_stay_days])
Revenue MoM % = DIVIDE([Total Revenue] - [Prev Month Revenue], [Prev Month Revenue], 0)
Prev Month Revenue = CALCULATE([Total Revenue], DATEADD(visits[visit_date], -1, MONTH))
```

## Report pages
1. **Executive Overview** — KPI cards (Total Visits, Revenue, Admission Rate, Avg LOS), monthly revenue line, department revenue bar
2. **Clinical Operations** — avg LOS by diagnosis (bar), admission rate by department, discharge status donut
3. **Doctors & Revenue** — top doctors table, revenue by specialization, consultation fee scatter
4. **Patients** — city distribution map, insurance provider share, age-band histogram

## Free alternative
No Power BI Desktop? Use **Power BI Service in free Microsoft account** trial, or replicate with Metabase/Apache Superset pointed at MySQL — same schema and DAX-typed metrics apply.
