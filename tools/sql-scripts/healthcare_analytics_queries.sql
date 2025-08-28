-- Healthcare Analytics SQL Scripts
-- Collection of reusable SQL queries for healthcare data analysis

-- Patient Demographics Summary
-- Provides overview of patient population by age groups and gender
WITH age_groups AS (
    SELECT 
        patient_id,
        CASE 
            WHEN age < 18 THEN 'Pediatric (0-17)'
            WHEN age BETWEEN 18 AND 34 THEN 'Young Adult (18-34)'
            WHEN age BETWEEN 35 AND 49 THEN 'Middle Age (35-49)'
            WHEN age BETWEEN 50 AND 64 THEN 'Older Adult (50-64)'
            WHEN age >= 65 THEN 'Senior (65+)'
        END AS age_group,
        gender
    FROM patients
)
SELECT 
    age_group,
    gender,
    COUNT(*) as patient_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM age_groups
GROUP BY age_group, gender
ORDER BY age_group, gender;

-- 30-Day Readmission Analysis
-- Identifies patients readmitted within 30 days
WITH readmissions AS (
    SELECT 
        a1.patient_id,
        a1.admission_date as first_admission,
        a1.discharge_date as first_discharge,
        a2.admission_date as readmission_date,
        DATEDIFF(day, a1.discharge_date, a2.admission_date) as days_between
    FROM admissions a1
    JOIN admissions a2 ON a1.patient_id = a2.patient_id
    WHERE a2.admission_date > a1.discharge_date
        AND DATEDIFF(day, a1.discharge_date, a2.admission_date) <= 30
)
SELECT 
    COUNT(DISTINCT patient_id) as readmitted_patients,
    COUNT(*) as total_readmissions,
    AVG(days_between) as avg_days_to_readmission
FROM readmissions;

-- Average Length of Stay by Department
-- Calculates average LOS for different departments
SELECT 
    department,
    COUNT(*) as total_admissions,
    AVG(DATEDIFF(day, admission_date, discharge_date)) as avg_length_of_stay,
    MIN(DATEDIFF(day, admission_date, discharge_date)) as min_los,
    MAX(DATEDIFF(day, admission_date, discharge_date)) as max_los,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY DATEDIFF(day, admission_date, discharge_date)) as median_los
FROM admissions a
JOIN departments d ON a.department_id = d.department_id
WHERE discharge_date IS NOT NULL
GROUP BY department
ORDER BY avg_length_of_stay DESC;

-- Monthly Patient Volume Trends
-- Shows patient admission trends over time
SELECT 
    YEAR(admission_date) as year,
    MONTH(admission_date) as month,
    COUNT(*) as admissions,
    COUNT(DISTINCT patient_id) as unique_patients,
    AVG(DATEDIFF(day, admission_date, COALESCE(discharge_date, GETDATE()))) as avg_los
FROM admissions
WHERE admission_date >= DATEADD(year, -2, GETDATE())
GROUP BY YEAR(admission_date), MONTH(admission_date)
ORDER BY year, month;

-- High-Risk Patient Identification
-- Identifies patients with multiple comorbidities or frequent admissions
WITH patient_risk AS (
    SELECT 
        p.patient_id,
        p.age,
        COUNT(DISTINCT a.admission_id) as admission_count,
        COUNT(DISTINCT d.diagnosis_code) as unique_diagnoses,
        MAX(a.admission_date) as last_admission
    FROM patients p
    LEFT JOIN admissions a ON p.patient_id = a.patient_id
    LEFT JOIN diagnoses d ON a.admission_id = d.admission_id
    WHERE a.admission_date >= DATEADD(year, -1, GETDATE())
    GROUP BY p.patient_id, p.age
)
SELECT 
    patient_id,
    age,
    admission_count,
    unique_diagnoses,
    last_admission,
    CASE 
        WHEN admission_count >= 4 AND unique_diagnoses >= 3 THEN 'High Risk'
        WHEN admission_count >= 2 OR unique_diagnoses >= 2 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_category
FROM patient_risk
WHERE admission_count > 0
ORDER BY admission_count DESC, unique_diagnoses DESC;

-- Department Efficiency Metrics
-- Compares department performance metrics
SELECT 
    d.department_name,
    COUNT(a.admission_id) as total_cases,
    AVG(DATEDIFF(day, a.admission_date, a.discharge_date)) as avg_los,
    SUM(CASE WHEN DATEDIFF(day, a.discharge_date, ra.admission_date) <= 30 
             THEN 1 ELSE 0 END) * 100.0 / COUNT(a.admission_id) as readmission_rate,
    AVG(ps.satisfaction_score) as avg_satisfaction
FROM departments d
JOIN admissions a ON d.department_id = a.department_id
LEFT JOIN admissions ra ON a.patient_id = ra.patient_id 
    AND ra.admission_date > a.discharge_date
    AND DATEDIFF(day, a.discharge_date, ra.admission_date) <= 30
LEFT JOIN patient_satisfaction ps ON a.admission_id = ps.admission_id
WHERE a.discharge_date IS NOT NULL
    AND a.admission_date >= DATEADD(year, -1, GETDATE())
GROUP BY d.department_id, d.department_name
ORDER BY readmission_rate, avg_los;

-- Financial Performance by Service Line
-- Analyzes revenue and cost metrics
SELECT 
    sl.service_line_name,
    COUNT(a.admission_id) as case_volume,
    SUM(b.total_charges) as total_revenue,
    AVG(b.total_charges) as avg_revenue_per_case,
    SUM(b.total_costs) as total_costs,
    AVG(b.total_costs) as avg_cost_per_case,
    (SUM(b.total_charges) - SUM(b.total_costs)) as net_margin,
    ((SUM(b.total_charges) - SUM(b.total_costs)) * 100.0 / SUM(b.total_charges)) as margin_percentage
FROM service_lines sl
JOIN admissions a ON sl.service_line_id = a.service_line_id
JOIN billing b ON a.admission_id = b.admission_id
WHERE a.admission_date >= DATEADD(month, -12, GETDATE())
GROUP BY sl.service_line_id, sl.service_line_name
HAVING COUNT(a.admission_id) >= 10  -- Minimum case volume for analysis
ORDER BY margin_percentage DESC;
