-- Healthcare Analytics - KPI queries
USE healthcare_db;

-- 1) Monthly revenue trend (FY 2024-2025)
SELECT DATE_FORMAT(visit_date, '%Y-%m') AS month,
       COUNT(*) AS visits,
       ROUND(SUM(treatment_cost_inr),2) AS revenue_inr
FROM visits
GROUP BY month
ORDER BY month;

-- 2) Revenue + admission rate by department
SELECT d.department_name,
       COUNT(v.visit_id) AS total_visits,
       SUM(v.admitted_flag) AS admissions,
       ROUND(100 * SUM(v.admitted_flag) / COUNT(v.visit_id), 2) AS admission_rate_pct,
       ROUND(SUM(v.treatment_cost_inr),2) AS revenue_inr
FROM visits v
JOIN departments d ON v.department_id = d.department_id
GROUP BY d.department_name
ORDER BY revenue_inr DESC;

-- 3) Average length of stay by diagnosis (admitted only)
SELECT diagnosis,
       COUNT(*) AS admissions,
       ROUND(AVG(length_of_stay_days),1) AS avg_los
FROM visits
WHERE admitted_flag = 1
GROUP BY diagnosis
ORDER BY avg_los DESC;

-- 4) Top doctors by revenue and visit volume
SELECT dr.doctor_name,
       dr.specialization,
       COUNT(v.visit_id) AS visits,
       ROUND(SUM(v.treatment_cost_inr),2) AS revenue_inr
FROM visits v
JOIN doctors dr ON v.doctor_id = dr.doctor_id
GROUP BY dr.doctor_name, dr.specialization
ORDER BY revenue_inr DESC
LIMIT 10;

-- 5) Payment mix (Insurance vs Cash vs Card vs UPI)
SELECT payment_method,
       COUNT(*) AS visits,
       ROUND(SUM(treatment_cost_inr),2) AS revenue_inr,
       ROUND(SUM(treatment_cost_inr) * 100 / SUM(SUM(treatment_cost_inr)) OVER (), 2) AS revenue_share_pct
FROM visits
GROUP BY payment_method
ORDER BY revenue_inr DESC;

-- 6) Bed occupancy proxy: avg concurrent admissions per month
SELECT DATE_FORMAT(visit_date, '%Y-%m') AS month,
       ROUND(AVG(length_of_stay_days),1) AS avg_los,
       COUNT(DISTINCT patient_id) AS unique_patients
FROM visits
WHERE admitted_flag = 1
GROUP BY month
ORDER BY month;

-- 7) Discharge status distribution (admissions)
SELECT discharge_status, COUNT(*) AS count_,
       ROUND(COUNT(*)*100/SUM(COUNT(*)) OVER (),2) AS pct
FROM visits
WHERE admitted_flag = 1
GROUP BY discharge_status
ORDER BY count_ DESC;

-- 8) City-wise patient distribution
SELECT city, COUNT(*) AS patients
FROM patients
GROUP BY city
ORDER BY patients DESC;
