-- Healthcare Analytics - schema for hospital operations analysis
CREATE DATABASE IF NOT EXISTS healthcare_db;
USE healthcare_db;

CREATE TABLE departments (
    department_id VARCHAR(5) PRIMARY KEY,
    department_name VARCHAR(50),
    dept_code VARCHAR(10),
    floor INT,
    head_doctor_id VARCHAR(8),
    annual_budget_inr DECIMAL(15,2)
);

CREATE TABLE doctors (
    doctor_id VARCHAR(6) PRIMARY KEY,
    doctor_name VARCHAR(80),
    specialization VARCHAR(60),
    department_id VARCHAR(5),
    years_experience INT,
    consultation_fee_inr DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE patients (
    patient_id VARCHAR(7) PRIMARY KEY,
    name VARCHAR(90),
    gender CHAR(1),
    age INT,
    city VARCHAR(30),
    insurance_provider VARCHAR(40),
    blood_group VARCHAR(4)
);

CREATE TABLE visits (
    visit_id VARCHAR(8) PRIMARY KEY,
    patient_id VARCHAR(7),
    doctor_id VARCHAR(6),
    department_id VARCHAR(5),
    visit_date DATE,
    diagnosis VARCHAR(50),
    treatment_cost_inr DECIMAL(12,2),
    admitted_flag TINYINT,
    length_of_stay_days INT,
    discharge_status VARCHAR(20),
    payment_method VARCHAR(15),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    INDEX idx_visit_date (visit_date),
    INDEX idx_department (department_id)
);

-- MySQL bulk import (adjust secure_file_priv path as needed)
LOAD DATA INFILE 'visits.csv' INTO TABLE visits
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE 'patients.csv' INTO TABLE patients
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE 'doctors.csv' INTO TABLE doctors
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
LOAD DATA INFILE 'departments.csv' INTO TABLE departments
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
