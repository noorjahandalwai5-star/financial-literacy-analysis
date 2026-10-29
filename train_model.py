"""
Financial Literacy Project - Machine Learning Classification Pipeline
Author: B.Sc Data Science Student
Description:
    Trains an explainable Decision Tree Classifier to predict a student's
    Financial Literacy Level (Basic, Intermediate, Advanced) based on their
    academic stage, financial habits, and awareness indicators.
    
    Data Leakage Prevention:
    The continuous 'Financial_Literacy_Score' is strictly EXCLUDED from features.
"""

import os
import json
import pandas as pd
import numpy as np

# Machine Learning imports
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import OrdinalEncoder
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "financial_literacy.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "decision_tree_model.joblib")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")

os.makedirs(MODEL_DIR, exist_ok=True)

# Selected features (NO DATA LEAKAGE: exclude Financial_Literacy_Score and Student_ID)
FEATURE_COLUMNS = [
    "Age_Group",
    "Course",
    "Year_of_Study",
    "Financial_Education",
    "Budgeting_Habit",
    "Saving_Habit",
    "Monthly_Expense_Category",
    "Emergency_Fund_Awareness",
    "Risk_Awareness"
]

TARGET_COLUMN = "Financial_Literacy_Level"

def train_and_evaluate():
    print("=" * 65)
    print("   FINANCIAL LITERACY - MACHINE LEARNING MODEL TRAINING")
    print("=" * 65)
    
    # 1. Load Cleaned Dataset
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}. Run data_processing.py first.")
    
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded dataset with {len(df)} student records.")
    
    # 2. Separate Features (X) and Target (y)
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    
    print(f"Features used ({len(FEATURE_COLUMNS)}): {FEATURE_COLUMNS}")
    print(f"Target variable : {TARGET_COLUMN} (Classes: {list(y.unique())})")
    print("-" * 65)
    
    # 3. Categorical Encoding using OrdinalEncoder
    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    X_encoded = encoder.fit_transform(X)
    X_encoded_df = pd.DataFrame(X_encoded, columns=FEATURE_COLUMNS)
    
    # 4. Train-Test Split (80% Train, 20% Test, Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded_df, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training Samples : {len(X_train)} (80%)")
    print(f"Testing Samples  : {len(X_test)} (20%)")
    print("-" * 65)
    
    # 5. Train Decision Tree Classifier (max_depth=4 for human explainability)
    dt_classifier = DecisionTreeClassifier(
        criterion="gini",
        max_depth=4,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    dt_classifier.fit(X_train, y_train)
    
    # 6. Evaluate Decision Tree
    y_pred_dt = dt_classifier.predict(X_test)
    dt_accuracy = accuracy_score(y_test, y_pred_dt)
    
    print("1. DECISION TREE CLASSIFIER EVALUATION:")
    print(f"   Accuracy: {dt_accuracy * 100:.2f}%")
    print("\nClassification Report (Decision Tree):")
    print(classification_report(y_test, y_pred_dt, zero_division=0))
    print("Confusion Matrix (Decision Tree):")
    cm = confusion_matrix(y_test, y_pred_dt, labels=["Basic", "Intermediate", "Advanced"])
    print(pd.DataFrame(cm, index=["Actual Basic", "Actual Inter.", "Actual Adv."],
                         columns=["Pred Basic", "Pred Inter.", "Pred Adv."]))
    print("-" * 65)
    
    # 7. Compare with Random Forest Classifier (for academic comparison)
    rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf_classifier.fit(X_train, y_train)
    y_pred_rf = rf_classifier.predict(X_test)
    rf_accuracy = accuracy_score(y_test, y_pred_rf)
    
    print("2. RANDOM FOREST CLASSIFIER (COMPARISON):")
    print(f"   Accuracy: {rf_accuracy * 100:.2f}%")
    print(f"   Performance Delta: {(rf_accuracy - dt_accuracy) * 100:+.2f}%")
    print("-" * 65)
    
    # 8. Feature Importance
    feature_importances = dict(zip(FEATURE_COLUMNS, dt_classifier.feature_importances_))
    sorted_importances = sorted(feature_importances.items(), key=lambda x: x[1], reverse=True)
    
    print("Feature Importance Ranking (Decision Tree):")
    for feat, imp in sorted_importances:
        print(f"   - {feat:<28}: {imp * 100:.2f}%")
    print("-" * 65)
    
    # 9. Save Model and Metadata
    model_payload = {
        "model": dt_classifier,
        "encoder": encoder,
        "feature_columns": FEATURE_COLUMNS,
        "classes": list(dt_classifier.classes_)
    }
    joblib.dump(model_payload, MODEL_PATH)
    print(f"[OK] Trained model successfully saved to: {MODEL_PATH}")
    
    metadata = {
        "model_name": "DecisionTreeClassifier",
        "parameters": {"max_depth": 4, "criterion": "gini", "min_samples_split": 10},
        "dt_accuracy": round(float(dt_accuracy * 100), 2),
        "rf_accuracy": round(float(rf_accuracy * 100), 2),
        "feature_columns": FEATURE_COLUMNS,
        "feature_importances": {feat: round(float(imp * 100), 2) for feat, imp in sorted_importances},
        "categories": {col: [int(x) if isinstance(x, (np.integer, int)) else str(x) for x in encoder.categories_[idx]] for idx, col in enumerate(FEATURE_COLUMNS)},
        "classes": [str(c) for c in dt_classifier.classes_]
    }
    
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"[OK] Model metadata saved to: {METADATA_PATH}")
    print("=" * 65)

if __name__ == "__main__":
    train_and_evaluate()

