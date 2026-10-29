"""
Financial Literacy Project - Exploratory Data Analysis (EDA)
Author: B.Sc Data Science Student
Description:
    Performs comprehensive Exploratory Data Analysis on the survey responses.
    Answers core research questions:
    - What percentage demonstrate basic vs advanced knowledge?
    - How many students regularly budget and save?
    - Which financial topic has the highest knowledge gap?
    - How do scores vary across study years and prior financial education?
    - Is there a correlation between budgeting and literacy scores?
"""

import os
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "financial_literacy.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "static", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run data_processing.py first.")
    return pd.read_csv(DATA_PATH)

def perform_eda():
    df = load_data()
    print("=" * 65)
    print("   EXPLORATORY DATA ANALYSIS (EDA) REPORT")
    print("=" * 65)
    
    # 1. Overview Statistics
    total_responses = len(df)
    avg_score = round(df["Financial_Literacy_Score"].mean(), 2)
    median_score = round(df["Financial_Literacy_Score"].median(), 2)
    std_score = round(df["Financial_Literacy_Score"].std(), 2)
    
    print(f"Total Student Responses : {total_responses}")
    print(f"Mean Literacy Score     : {avg_score}%")
    print(f"Median Literacy Score   : {median_score}%")
    print(f"Score Std Deviation     : {std_score}%")
    print("-" * 65)

    # 2. Literacy Level Distribution
    level_dist = df["Financial_Literacy_Level"].value_counts(normalize=True).mul(100).round(1).to_dict()
    level_counts = df["Financial_Literacy_Level"].value_counts().to_dict()
    print("Financial Literacy Levels:")
    for lvl, pct in level_dist.items():
        print(f"  - {lvl:<14}: {level_counts[lvl]} students ({pct}%)")
    print("-" * 65)

    # 3. Knowledge Question Breakdown & Gap Analysis
    knowledge_topics = {
        "Digital_Payment_Knowledge": "Digital Payments & UPI Security",
        "Banking_Knowledge": "Basic Banking & Accounts",
        "Risk_Awareness": "Risk-Return Concept",
        "Loan_Knowledge": "Loans, Interest & Credit Score",
        "Emergency_Fund_Awareness": "Emergency Funds",
        "Interest_Rate_Knowledge": "Simple vs Compound Interest",
        "Inflation_Knowledge": "Inflation & Purchasing Power",
        "Investment_Knowledge": "Investments & Mutual Funds"
    }

    topic_pass_rates = {}
    for col, display_name in knowledge_topics.items():
        pass_rate = round(df[col].mean() * 100, 1)
        topic_pass_rates[display_name] = pass_rate

    # Sort topics by pass rate ascending (lowest pass rate = highest knowledge gap)
    sorted_gaps = sorted(topic_pass_rates.items(), key=lambda x: x[1])
    most_misunderstood = sorted_gaps[0][0]
    
    print("Topic Pass Rates (Knowledge Gaps):")
    for topic, rate in sorted_gaps:
        print(f"  - {topic:<34}: {rate}% pass rate (Gap: {round(100 - rate, 1)}%)")
    print(f"\n=> Most Misunderstood Topic: {most_misunderstood} ({sorted_gaps[0][1]}% pass rate)")
    print("-" * 65)

    # 4. Impact of Prior Financial Education
    edu_comparison = df.groupby("Financial_Education")["Financial_Literacy_Score"].agg(["mean", "median", "count"]).round(2).to_dict(orient="index")
    print("Impact of Prior Financial Education:")
    for edu_status, stats in edu_comparison.items():
        print(f"  - Prior Education: {edu_status:<4} | Avg Score: {stats['mean']}% | Students: {stats['count']}")
    print("-" * 65)

    # 5. Literacy by Year of Study
    year_comparison = df.groupby("Year_of_Study")["Financial_Literacy_Score"].agg(["mean", "count"]).round(2).to_dict(orient="index")
    print("Literacy by Year of Study:")
    for yr, stats in year_comparison.items():
        print(f"  - {yr:<10}: Avg Score {stats['mean']}% (N={stats['count']})")
    print("-" * 65)

    # 6. Budgeting & Saving Habits
    budget_dist = df["Budgeting_Habit"].value_counts(normalize=True).mul(100).round(1).to_dict()
    saving_dist = df["Saving_Habit"].value_counts(normalize=True).mul(100).round(1).to_dict()
    
    print("Budgeting Habits (% of students):")
    for habit, pct in budget_dist.items():
        print(f"  - {habit:<14}: {pct}%")
    print("\nSaving Habits (% of students):")
    for habit, pct in saving_dist.items():
        print(f"  - {habit:<26}: {pct}%")
    print("-" * 65)

    # 7. Export summary stats as JSON for Flask dashboard use
    summary_data = {
        "total_responses": total_responses,
        "avg_score": avg_score,
        "median_score": median_score,
        "std_score": std_score,
        "most_misunderstood": most_misunderstood,
        "level_counts": level_counts,
        "level_percentages": level_dist,
        "topic_pass_rates": topic_pass_rates,
        "edu_comparison": edu_comparison,
        "year_comparison": year_comparison,
        "budget_dist": budget_dist,
        "saving_dist": saving_dist
    }

    summary_file = os.path.join(DATA_PATH.replace("financial_literacy.csv", "eda_summary.json"))
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4)
        
    print(f"[OK] EDA summary successfully saved to: {summary_file}")
    print("=" * 65)
    return summary_data

if __name__ == "__main__":
    perform_eda()

