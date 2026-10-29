-- =====================================================================
-- Database Name: financial_literacy_db
-- Project: Financial Literacy Among College Students
-- Description: MySQL Schema, Sample Data, and Analytical Queries
-- =====================================================================

-- 1. Create and Select Database
CREATE DATABASE IF NOT EXISTS financial_literacy_db;
USE financial_literacy_db;

-- 2. Drop Table If Exists
DROP TABLE IF EXISTS student_responses;

-- 3. Create student_responses Table
CREATE TABLE student_responses (
    student_id VARCHAR(10) PRIMARY KEY,
    age_group VARCHAR(10) NOT NULL,
    course VARCHAR(50) NOT NULL,
    year_of_study VARCHAR(20) NOT NULL,
    financial_education ENUM('Yes', 'No') NOT NULL,
    budgeting_habit ENUM('Never', 'Rarely', 'Occasionally', 'Regularly') NOT NULL,
    monthly_expense_category VARCHAR(50) NOT NULL,
    saving_habit VARCHAR(50) NOT NULL,
    banking_knowledge TINYINT(1) NOT NULL DEFAULT 0,
    digital_payment_knowledge TINYINT(1) NOT NULL DEFAULT 0,
    interest_rate_knowledge TINYINT(1) NOT NULL DEFAULT 0,
    inflation_knowledge TINYINT(1) NOT NULL DEFAULT 0,
    loan_knowledge TINYINT(1) NOT NULL DEFAULT 0,
    investment_knowledge TINYINT(1) NOT NULL DEFAULT 0,
    risk_awareness TINYINT(1) NOT NULL DEFAULT 0,
    emergency_fund_awareness TINYINT(1) NOT NULL DEFAULT 0,
    financial_literacy_score DECIMAL(5, 2) NOT NULL,
    financial_literacy_level ENUM('Basic', 'Intermediate', 'Advanced') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- 4. Sample Insert Statements (First 10 Sample Records)
-- =====================================================================

INSERT INTO student_responses (
    student_id, age_group, course, year_of_study, financial_education,
    budgeting_habit, monthly_expense_category, saving_habit,
    banking_knowledge, digital_payment_knowledge, interest_rate_knowledge,
    inflation_knowledge, loan_knowledge, investment_knowledge,
    risk_awareness, emergency_fund_awareness, financial_literacy_score, financial_literacy_level
) VALUES
('STU0001', '18-19', 'B.A', '1st Year', 'No', 'Rarely', 'Shopping & Fashion', 'Saves Whatever is Left', 1, 1, 0, 0, 1, 0, 1, 1, 62.50, 'Intermediate'),
('STU0002', '18-19', 'B.A', '2nd Year', 'Yes', 'Occasionally', 'Travel & Commute', 'Invests Regularly', 1, 1, 1, 1, 0, 1, 0, 0, 62.50, 'Intermediate'),
('STU0003', '22-23', 'B.A', '4th Year', 'No', 'Occasionally', 'Food & Dining', 'Saves Whatever is Left', 1, 1, 1, 1, 1, 1, 0, 0, 75.00, 'Intermediate'),
('STU0004', '20-21', 'B.Sc Data Science', '3rd Year', 'Yes', 'Occasionally', 'Study Materials & Books', 'Saves a Fixed Percentage', 1, 1, 1, 1, 1, 1, 1, 1, 100.00, 'Advanced'),
('STU0005', '20-21', 'B.B.A', '3rd Year', 'Yes', 'Occasionally', 'Travel & Commute', 'Saves a Fixed Percentage', 1, 1, 1, 1, 1, 1, 0, 0, 75.00, 'Intermediate'),
('STU0006', '20-21', 'B.Sc Data Science', '2nd Year', 'No', 'Rarely', 'Study Materials & Books', 'Saves Whatever is Left', 1, 1, 0, 0, 0, 1, 0, 0, 37.50, 'Basic'),
('STU0007', '18-19', 'B.Sc Computer Science', '1st Year', 'No', 'Occasionally', 'Travel & Commute', 'Saves Whatever is Left', 1, 0, 0, 0, 0, 0, 0, 0, 12.50, 'Basic'),
('STU0008', '18-19', 'B.Sc Computer Science', '1st Year', 'No', 'Occasionally', 'Shopping & Fashion', 'Invests Regularly', 1, 1, 0, 1, 1, 0, 1, 0, 62.50, 'Intermediate'),
('STU0009', '20-21', 'B.Sc Mathematics', '1st Year', 'No', 'Never', 'Shopping & Fashion', 'Saves a Fixed Percentage', 1, 1, 0, 0, 1, 0, 1, 1, 62.50, 'Intermediate'),
('STU0010', '20-21', 'B.Com', '2nd Year', 'Yes', 'Regularly', 'Food & Dining', 'Saves a Fixed Percentage', 1, 1, 1, 0, 1, 1, 1, 1, 87.50, 'Advanced');

-- =====================================================================
-- 5. Beginner-Friendly Analytical SQL Queries (For College Viva)
-- =====================================================================

-- Query 1: Calculate Overall Average Financial Literacy Score
SELECT 
    COUNT(*) AS total_students_surveyed,
    ROUND(AVG(financial_literacy_score), 2) AS average_literacy_score,
    MIN(financial_literacy_score) AS minimum_score,
    MAX(financial_literacy_score) AS maximum_score
FROM student_responses;

-- Query 2: Distribution of Students Across Literacy Levels
SELECT 
    financial_literacy_level,
    COUNT(*) AS student_count,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM student_responses)), 1) AS percentage_share
FROM student_responses
GROUP BY financial_literacy_level
ORDER BY percentage_share DESC;

-- Query 3: Topic-wise Knowledge Pass Rates (Identifying Most Misunderstood Topics)
SELECT 
    'Digital Payments' AS topic, ROUND(AVG(digital_payment_knowledge) * 100, 1) AS pass_rate_pct FROM student_responses
UNION ALL
SELECT 'Basic Banking', ROUND(AVG(banking_knowledge) * 100, 1) FROM student_responses
UNION ALL
SELECT 'Risk-Return Concept', ROUND(AVG(risk_awareness) * 100, 1) FROM student_responses
UNION ALL
SELECT 'Emergency Funds', ROUND(AVG(emergency_fund_awareness) * 100, 1) FROM student_responses
UNION ALL
SELECT 'Loans & Credit', ROUND(AVG(loan_knowledge) * 100, 1) FROM student_responses
UNION ALL
SELECT 'Interest Rates', ROUND(AVG(interest_rate_knowledge) * 100, 1) FROM student_responses
UNION ALL
SELECT 'Inflation & Purchasing Power', ROUND(AVG(inflation_knowledge) * 100, 1) FROM student_responses
UNION ALL
SELECT 'Investments & Mutual Funds', ROUND(AVG(investment_knowledge) * 100, 1) FROM student_responses
ORDER BY pass_rate_pct ASC;

-- Query 4: Budgeting Habits by Year of Study
SELECT 
    year_of_study,
    budgeting_habit,
    COUNT(*) AS student_count
FROM student_responses
GROUP BY year_of_study, budgeting_habit
ORDER BY year_of_study, student_count DESC;

-- Query 5: Comparison of Students With vs Without Prior Financial Education
SELECT 
    financial_education,
    COUNT(*) AS student_count,
    ROUND(AVG(financial_literacy_score), 2) AS avg_score,
    ROUND(AVG(interest_rate_knowledge) * 100, 1) AS interest_knowledge_pct,
    ROUND(AVG(inflation_knowledge) * 100, 1) AS inflation_knowledge_pct,
    ROUND(AVG(investment_knowledge) * 100, 1) AS investment_knowledge_pct
FROM student_responses
GROUP BY financial_education;

