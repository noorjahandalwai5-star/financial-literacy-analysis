"""
Financial Literacy Project - Database Helper Module
Author: B.Sc Data Science Student
Description:
    Connects to MySQL database if available, with an automatic fallback
    to the CSV file. This guarantees that your Flask application runs smoothly
    even if MySQL is temporarily offline during a college presentation.
"""

import os
import pandas as pd

# MySQL Configuration (Change credentials if your local MySQL uses different ones)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "financial_literacy_db"
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "financial_literacy.csv")

def get_db_connection():
    """Attempts to establish a connection to MySQL. Returns None if connection fails."""
    try:
        import mysql.connector
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Exception:
        return None
    return None

def fetch_all_responses():
    """
    Fetches all student survey responses.
    Checks MySQL first. If unavailable, reads directly from CSV.
    """
    conn = get_db_connection()
    if conn:
        try:
            query = "SELECT * FROM student_responses ORDER BY student_id ASC"
            df = pd.read_sql(query, conn)
            conn.close()
            return df, "MySQL Database (Live)"
        except Exception:
            if conn:
                conn.close()
                
    # Fallback to CSV
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        return df, "Local CSV File (Offline Mode)"
    else:
        return pd.DataFrame(), "No Data Source Found"

def insert_student_response(record):
    """
    Inserts a newly surveyed student record into MySQL if connected,
    and appends to the local CSV.
    """
    # 1. Append to CSV
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df_new = pd.DataFrame([record])
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)
        
    # 2. Insert to MySQL if available
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO student_responses (
                student_id, age_group, course, year_of_study, financial_education,
                budgeting_habit, monthly_expense_category, saving_habit,
                banking_knowledge, digital_payment_knowledge, interest_rate_knowledge,
                inflation_knowledge, loan_knowledge, investment_knowledge,
                risk_awareness, emergency_fund_awareness, financial_literacy_score, financial_literacy_level
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                record.get("Student_ID"), record.get("Age_Group"), record.get("Course"),
                record.get("Year_of_Study"), record.get("Financial_Education"),
                record.get("Budgeting_Habit"), record.get("Monthly_Expense_Category"),
                record.get("Saving_Habit"), record.get("Banking_Knowledge", 0),
                record.get("Digital_Payment_Knowledge", 0), record.get("Interest_Rate_Knowledge", 0),
                record.get("Inflation_Knowledge", 0), record.get("Loan_Knowledge", 0),
                record.get("Investment_Knowledge", 0), record.get("Risk_Awareness", 0),
                record.get("Emergency_Fund_Awareness", 0), record.get("Financial_Literacy_Score", 0),
                record.get("Financial_Literacy_Level", "Basic")
            )
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception:
            if conn:
                conn.close()
    return True

