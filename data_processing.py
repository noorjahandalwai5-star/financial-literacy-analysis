"""
Financial Literacy Project - Data Generation & Processing Pipeline
Author: B.Sc Data Science Student
Description:
    Generates a realistic synthetic dataset (N=600) representing college students
    across various streams and years. Calculates objective financial literacy scores,
    cleans and validates the data, and exports both CSV and Excel files.
"""

import os
import random
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_PATH = os.path.join(DATA_DIR, "financial_literacy.csv")
EXCEL_PATH = os.path.join(DATA_DIR, "financial_literacy.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 1. SURVEY QUESTIONS & SCORING RUBRIC DEFINITION
# -------------------------------------------------------------------------
"""
Quiz Topics & Scoring Rubric:
Each knowledge question is scored as 1 (Correct / Aware) or 0 (Incorrect / Unaware).
Total score is out of 8 points, converted to a percentage (0-100%).

Topics Evaluated:
1. Banking_Knowledge: Understanding savings accounts, debit cards, IFSC, and NEFT/RTGS.
2. Digital_Payment_Knowledge: Safe UPI usage, 2FA, OTP security.
3. Interest_Rate_Knowledge: Difference between simple and compound interest; loan APR.
4. Inflation_Knowledge: Impact of inflation on purchasing power over time.
5. Loan_Knowledge: Credit score impact, collateral, difference between good and bad debt.
6. Investment_Knowledge: Basic understanding of Mutual Funds, Stocks, and Fixed Deposits.
7. Risk_Awareness: Risk-return relationship (higher returns usually carry higher risk).
8. Emergency_Fund_Awareness: Need to maintain 3-6 months of living expenses in liquid funds.

Literacy Levels:
- Basic        : Score < 50%   (< 4 / 8)
- Intermediate : 50% <= Score <= 75%  (4 to 6 / 8)
- Advanced     : Score > 75%   (7 or 8 / 8)
"""

COURSES = ["B.Sc Data Science", "B.Sc Computer Science", "B.Com", "B.B.A", "B.A", "B.Tech", "B.Sc Mathematics"]
YEARS = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
AGE_GROUPS = ["18-19", "20-21", "22-23", "24+"]
EXPENSE_CATEGORIES = ["Food & Dining", "Travel & Commute", "Entertainment & Leisure", "Study Materials & Books", "Shopping & Fashion"]
BUDGETING_HABITS = ["Never", "Rarely", "Occasionally", "Regularly"]
SAVING_HABITS = ["Does Not Save", "Saves Whatever is Left", "Saves a Fixed Percentage", "Invests Regularly"]

def generate_student_record(student_id):
    """Generates a realistic student survey response with realistic behavioral correlations."""
    
    # 1. Demographics
    course = random.choice(COURSES)
    year = random.choice(YEARS)
    
    if year == "1st Year":
        age_group = random.choice(["18-19", "18-19", "20-21"])
    elif year == "2nd Year":
        age_group = random.choice(["18-19", "20-21", "20-21"])
    elif year == "3rd Year":
        age_group = random.choice(["20-21", "20-21", "22-23"])
    else:
        age_group = random.choice(["20-21", "22-23", "24+"])
        
    # Prior financial education (commerce / business students have higher prior exposure)
    if course in ["B.Com", "B.B.A"]:
        fin_edu_prob = 0.65
    elif course in ["B.Sc Data Science", "B.Tech"]:
        fin_edu_prob = 0.40
    else:
        fin_edu_prob = 0.25
        
    financial_education = "Yes" if random.random() < fin_edu_prob else "No"
    
    # 2. Knowledge Probabilities (conditioned on Year of study & Prior Financial Education)
    base_boost = 0.15 if financial_education == "Yes" else 0.0
    year_boost = {"1st Year": 0.0, "2nd Year": 0.08, "3rd Year": 0.15, "4th Year": 0.22}[year]
    
    # Banking & UPI are widely understood due to daily smartphone usage
    p_banking = min(0.95, 0.70 + base_boost + year_boost)
    p_digital = min(0.98, 0.85 + (base_boost * 0.5) + (year_boost * 0.5))
    
    # Inflation and Interest Rates are classic student knowledge gaps
    p_interest = min(0.85, 0.35 + base_boost + year_boost)
    p_inflation = min(0.80, 0.30 + base_boost + year_boost)
    
    # Loans & Investments
    p_loans = min(0.80, 0.38 + base_boost + year_boost)
    p_investment = min(0.75, 0.28 + base_boost + year_boost)
    p_risk = min(0.82, 0.42 + base_boost + year_boost)
    p_emergency = min(0.78, 0.35 + base_boost + year_boost)
    
    # 3. Knowledge Responses (1 = Correct, 0 = Incorrect)
    k_banking = 1 if random.random() < p_banking else 0
    k_digital = 1 if random.random() < p_digital else 0
    k_interest = 1 if random.random() < p_interest else 0
    k_inflation = 1 if random.random() < p_inflation else 0
    k_loans = 1 if random.random() < p_loans else 0
    k_investment = 1 if random.random() < p_investment else 0
    k_risk = 1 if random.random() < p_risk else 0
    k_emergency = 1 if random.random() < p_emergency else 0
    
    # 4. Habits (influenced by education and maturity)
    if financial_education == "Yes" and (k_banking + k_investment >= 1):
        budget_habit = random.choices(BUDGETING_HABITS, weights=[0.1, 0.2, 0.35, 0.35])[0]
        saving_habit = random.choices(SAVING_HABITS, weights=[0.05, 0.30, 0.40, 0.25])[0]
    else:
        budget_habit = random.choices(BUDGETING_HABITS, weights=[0.35, 0.35, 0.20, 0.10])[0]
        saving_habit = random.choices(SAVING_HABITS, weights=[0.30, 0.45, 0.20, 0.05])[0]
        
    monthly_expense_cat = random.choice(EXPENSE_CATEGORIES)
    
    # 5. Compute Financial Literacy Score (Sum out of 8, converted to Percentage)
    raw_score = (k_banking + k_digital + k_interest + k_inflation + 
                 k_loans + k_investment + k_risk + k_emergency)
    score_percentage = round((raw_score / 8.0) * 100, 1)
    
    # 6. Assign Target Level
    if score_percentage < 50.0:
        level = "Basic"
    elif score_percentage <= 75.0:
        level = "Intermediate"
    else:
        level = "Advanced"
        
    return {
        "Student_ID": f"STU{student_id:04d}",
        "Age_Group": age_group,
        "Course": course,
        "Year_of_Study": year,
        "Financial_Education": financial_education,
        "Budgeting_Habit": budget_habit,
        "Monthly_Expense_Category": monthly_expense_cat,
        "Saving_Habit": saving_habit,
        "Banking_Knowledge": k_banking,
        "Digital_Payment_Knowledge": k_digital,
        "Interest_Rate_Knowledge": k_interest,
        "Inflation_Knowledge": k_inflation,
        "Loan_Knowledge": k_loans,
        "Investment_Knowledge": k_investment,
        "Risk_Awareness": k_risk,
        "Emergency_Fund_Awareness": k_emergency,
        "Financial_Literacy_Score": score_percentage,
        "Financial_Literacy_Level": level
    }

def clean_and_validate_dataset(df):
    """
    Performs data cleaning:
    - Checks and eliminates duplicate student entries
    - Checks and handles missing values
    - Validates data types and value ranges
    - Standardizes text columns
    """
    initial_count = len(df)
    
    # 1. Remove duplicate IDs if any
    df = df.drop_duplicates(subset=["Student_ID"])
    
    # 2. Check missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        df = df.dropna()
        
    # 3. Standardize text values (strip whitespace)
    text_cols = ["Age_Group", "Course", "Year_of_Study", "Financial_Education", 
                 "Budgeting_Habit", "Monthly_Expense_Category", "Saving_Habit", "Financial_Literacy_Level"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        
    # 4. Range validation
    df = df[(df["Financial_Literacy_Score"] >= 0) & (df["Financial_Literacy_Score"] <= 100)]
    
    print(f"Data Cleaning Complete: {len(df)} valid records retained from {initial_count} initial records.")
    return df

def main():
    print("=" * 60)
    print("   GENERATING SYNTHETIC SURVEY DATASET (N=600)")
    print("=" * 60)
    
    records = [generate_student_record(i) for i in range(1, 601)]
    df_raw = pd.DataFrame(records)
    
    # Clean and validate
    df_cleaned = clean_and_validate_dataset(df_raw)
    
    # Export to CSV
    df_cleaned.to_csv(CSV_PATH, index=False)
    print(f"[OK] Exported CSV to: {CSV_PATH}")
    
    # Export to Excel for Power BI
    df_cleaned.to_excel(EXCEL_PATH, index=False, engine="openpyxl")
    print(f"[OK] Exported Excel to: {EXCEL_PATH}")
    
    # Print sample breakdown
    print("\nDataset Summary:")
    print(f"- Total Students: {len(df_cleaned)}")
    print(f"- Average Financial Literacy Score: {df_cleaned['Financial_Literacy_Score'].mean():.2f}%")
    print("\nDistribution by Literacy Level:")
    print(df_cleaned["Financial_Literacy_Level"].value_counts(normalize=True).mul(100).round(1).to_string())
    print("\nKnowledge Question Pass Rates:")
    k_cols = [
        "Digital_Payment_Knowledge", "Banking_Knowledge", "Risk_Awareness",
        "Loan_Knowledge", "Emergency_Fund_Awareness", "Interest_Rate_Knowledge",
        "Inflation_Knowledge", "Investment_Knowledge"
    ]
    for col in k_cols:
        rate = df_cleaned[col].mean() * 100
        print(f"  {col:<30}: {rate:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()

