import csv, random, datetime
from pathlib import Path

random.seed(42)
OUT = Path(__file__).resolve().parents[1] / 'data'
OUT.mkdir(parents=True, exist_ok=True)

depts = [('Cardiology','CARD-01'),('Orthopedics','ORTH-02'),('Pediatrics','PEDS-03'),('Neurology','NEUR-04'),('Emergency','EMER-05'),('Oncology','ONCO-06'),('General Medicine','GENM-07'),('Gynecology','GYNC-08')]
specs = ['Cardiologist','Orthopedic Surgeon','Pediatrician','Neurologist','Emergency Physician','Oncologist','General Physician','Gynecologist']
first = ['Rahul','Priya','Amit','Sneha','Vikram','Neha','Arjun','Kavya','Rohit','Anjali','Manish','Divya','Sanjay','Pooja','Karthik','Meera','Ishaan','Riya','Aditya','Tanvi']
last = ['Sharma','Verma','Iyer','Rao','Kapoor','Mehta','Nair','Reddy','Khan','Singh','Patil','Joshi','Gupta','Das','Bose','Chopra','Malhotra','Bhat','Pillai','Shah']
cities = ['Mumbai','Delhi','Bangalore','Hyderabad','Chennai','Kolkata','Pune','Ahmedabad','Jaipur','Lucknow']
departments = []
for i,(d,code) in enumerate(depts):
    departments.append({'department_id':f'D{i+1:02d}','department_name':d,'dept_code':code,'floor':10+i,'head_doctor_id':f'DR{i+3:03d}','annual_budget_inr':random.randint(80000000,250000000)})
doctors = []
for i in range(80):
    d = random.choice(departments)
    doctors.append({'doctor_id':f'DR{i+1:03d}','doctor_name':f'Dr. {random.choice(first)} {random.choice(last)}','specialization':specs[[x[0] for x in depts].index(d['department_name'])],'department_id':d['department_id'],'years_experience':random.randint(1,32),'consultation_fee_inr':random.choice([500,700,900,1200,1500,2000])})
patients = []
for i in range(5000):
    patients.append({'patient_id':f'PT{i+1:05d}','name':f'{random.choice(first)} {random.choice(last)}','gender':random.choice(['M','F']),'age':random.randint(1,89),'city':random.choice(cities),'insurance_provider':random.choice(['Star Health','HDFC Ergo','Niva Bupa','Care Health','ICICI Lombard','Self Pay']),'blood_group':random.choice(['A+','A-','B+','B-','O+','O-','AB+','AB-'])})
conditions = {'Cardiology':['Hypertension','Arrhythmia','CAD','Heart Failure'],'Orthopedics':['Fracture','Arthritis','Back Pain','Ligament Tear'],'Pediatrics':['Fever','Asthma','Vaccination','Viral Infection'],'Neurology':['Migraine','Stroke','Epilepsy','Neuropathy'],'Emergency':['Trauma','Burns','Poisoning','Severe Bleeding'],'Oncology':['Chemotherapy','Radiotherapy','Tumor Screening','Post-op Care'],'General Medicine':['Fever','Diabetes','Thyroid','Infection'],'Gynecology':['Prenatal Care','PCOS','Fertility','Menstrual Disorder']}
visits = []
vid = 1
dept_doc_map = {}
for doc in doctors:
    dept_doc_map.setdefault(doc['department_id'], []).append(doc['doctor_id'])
for _ in range(12000):
    d = random.choice(departments)
    dt = datetime.date(2024,1,1) + datetime.timedelta(days=random.randint(0,729))
    admission = random.random() < 0.18
    len_stay = random.randint(0,12) if admission else 0
    diag = random.choice(conditions[d['department_name']])
    cost = random.randint(30000,800000) if admission else random.randint(500,8000)
    visits.append({'visit_id':f'V{vid:06d}','patient_id':random.choice(patients)['patient_id'],'doctor_id':random.choice(dept_doc_map[d['department_id']]),'department_id':d['department_id'],'visit_date':dt.isoformat(),'diagnosis':diag,'treatment_cost_inr':cost,'admitted_flag':1 if admission else 0,'length_of_stay_days':len_stay,'discharge_status':random.choices(['Normal','Referred','LAMA','Expired'],weights=[0.86,0.08,0.04,0.02])[0] if admission else 'Not Admitted','payment_method':random.choice(['Insurance','Cash','Card','UPI'])})
    vid += 1
for name, rows in [('departments',departments),('doctors',doctors),('patients',patients),('visits',visits)]:
    with open(OUT/f'{name}.csv','w',newline='',encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(name, len(rows))
