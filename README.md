# Financial Literacy Among College Students: A Data Science & Machine Learning Analysis

**B.Sc Data Science Final Year / Degree Project**

---

## 1. Project Overview
This project presents an empirical, end-to-end data science study analyzing **Financial Literacy Among College Students**. It examines undergraduate students' understanding of personal finance, banking protocols, interest rates, inflation, debt management, and investment instruments.

### Key Objectives
- Identify the most acute financial knowledge gaps among undergraduate students.
- Analyze real-world correlations between prior financial education, academic seniority, and budgeting discipline.
- Deploy an explainable **Decision Tree Classifier** to categorize students into **Basic**, **Intermediate**, and **Advanced** literacy levels (strictly without data leakage).
- Provide an interactive web dashboard using **Flask**, **Bootstrap 5**, and **Chart.js**, backed by a **MySQL** relational database and **Power BI** business intelligence reporting.

---

## 2. Project Directory Structure

```text
financial-literacy-project/
├── app.py                      # Main Flask Web Application (7 pages)
├── data_processing.py          # Data Generation, Cleaning & Scoring Pipeline
├── analysis.py                 # Exploratory Data Analysis & Statistics Engine
├── train_model.py              # ML Model Training (Decision Tree & Random Forest)
├── verify_setup.py             # Environment Verification Script
├── requirements.txt            # Python Dependencies
├── README.md                   # Complete Documentation & Viva Guide
├── data/
│   ├── financial_literacy.csv  # Anonymized Student Survey Dataset (N=500)
│   └── eda_summary.json        # Precomputed Summary Statistics for Visuals
├── model/
│   ├── decision_tree_model.joblib # Serialized Trained ML Model
│   └── model_metadata.json     # Feature Importances & Model Evaluation Metrics
├── database/
│   ├── database.sql            # MySQL Schema, Inserts & 5 Viva Analytical Queries
│   └── db_helper.py            # MySQL Driver with Automatic CSV Fallback
├── templates/
│   ├── base.html               # Base Jinja2 Layout with Navbar & Footer
│   ├── index.html              # Page 1: Home & Overview
│   ├── dashboard.html          # Page 2: Executive KPI Dashboard & Chart.js
│   ├── data.html               # Page 3: Filterable & Searchable Survey Table
│   ├── analytics.html          # Page 4: In-depth EDA & Knowledge Gap Ranking
│   ├── prediction.html         # Page 5: Interactive ML Literacy Predictor Form
│   ├── education.html          # Page 6: Financial Concepts & Educational Guides
│   └── about.html              # Page 7: Methodology, Stack & Limitations
└── static/
    ├── css/
    │   └── style.css           # Custom Modern Styling
    └── js/
        └── script.js           # Chart.js Renderers & Live Table Filters
```

---

## 3. Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, Chart.js, FontAwesome 6.
- **Backend**: Python 3.10+, Flask 3.0.
- **Data Science**: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Joblib.
- **Database**: MySQL 8.0, `mysql-connector-python`.
- **Business Intelligence**: Microsoft Excel, Microsoft Power BI.

---

## 4. Setup and Execution Instructions

### Step 1: Open Terminal in VS Code
Navigate to the project folder:
```powershell
cd "C:\Users\noorjahan dalwai\.gemini\antigravity\scratch\financial-literacy-project"
```

### Step 2: Set Up Python Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Packages
```powershell
pip install -r requirements.txt
```

### Step 4: Verify Environment Setup
```powershell
python verify_setup.py
```

### Step 5: (Optional) Retrain Machine Learning Model
```powershell
python train_model.py
```

### Step 6: Launch the Web Application

#### Option A: Flask Web Dashboard (Recommended for Local Demo)
```powershell
python app.py
```
Open your browser at: **`http://127.0.0.1:5000`**

#### Option B: Streamlit Web Dashboard (For Cloud Deployment)
```powershell
streamlit run streamlit_app.py
```
> **Streamlit Community Cloud Notice:** When deploying on [share.streamlit.io](https://share.streamlit.io), ensure the **Main file path** is set to `streamlit_app.py` (not `app.py`).

---

## 5. MySQL Database Setup

1. Open **MySQL Workbench** or your command line client.
2. Execute the script located in `database/database.sql`:
   ```sql
   SOURCE database/database.sql;
   ```
3. The database `financial_literacy_db` and table `student_responses` will be created with sample records and 5 pre-built viva analytical queries.

---

## 6. Power BI Dashboard Setup

1. Open **Power BI Desktop**.
2. Click **Get Data > Text/CSV** and select `data/financial_literacy.csv`.
3. Add the following visuals:
   - **KPI Card 1**: `Total Students` = `COUNTROWS('financial_literacy')`
   - **KPI Card 2**: `Average Score` = `AVERAGE('financial_literacy'[Financial_Literacy_Score])`
   - **Donut Chart**: `Financial_Literacy_Level` as Legend, Count of `Student_ID` as Values.
   - **Bar Chart**: Topic Pass Rates (`Digital_Payment_Knowledge`, `Banking_Knowledge`, etc.).
   - **Slicers**: Add slicers for `Course`, `Year_of_Study`, and `Financial_Education`.

---

## 7. Viva Voce Preparation Guide (B.Sc Data Science Examination)

### Q1. What is Financial Literacy?
- **English**: Financial literacy is the ability to understand and effectively use various financial skills, including personal financial management, budgeting, saving, understanding interest, managing debt, and investing.
- **Roman English / Hinglish**: Financial literacy ka simple matlab hai apne paise ko samajhna aur sahi tareeqe se manage karna—jaise budget banana, fizool kharch bachana, compound interest samajhna, aur safe investments karna.

### Q2. Why did you choose this topic for your Data Science project?
- **English**: College students represent the immediate future workforce. However, many transition into financial independence without formal money management skills. We chose this project to empirically analyze where students struggle the most (e.g. investments and inflation) so targeted educational interventions can be developed.
- **Roman English**: College ke students jald hi earn karna shuru karenge, lekin unhe budgeting ya inflation ki practical knowledge nahi hoti. Data science ki madad se humne identify kiya ki students ko sabse zyada difficulty kis topic mein aati hai.

### Q3. What is Data Cleaning and why was it necessary?
- **English**: Data cleaning involves identifying and rectifying errors, missing entries, duplicates, and inconsistent formats before running analysis or machine learning algorithms. In our project, we verified that there were no duplicate student IDs, validated that score values were strictly between 0 and 100, and standardized categorical strings.
- **Roman English**: Data cleaning ka matlab raw dataset se duplicates, missing values aur wrong entries ko hatana. Agar raw data ganda hoga to model ki accuracy aur findings bhi galat hongi (Garbage In, Garbage Out).

### Q4. What is Exploratory Data Analysis (EDA)?
- **English**: EDA is an analytical approach to summarizing the main characteristics of a dataset, often using visual methods. In our project, EDA revealed that **Investments & Mutual Funds** is the most misunderstood topic (lowest pass rate), and students with prior financial education score ~14.8% higher.
- **Roman English**: EDA ka matlab data ko visual charts aur statistics ki madad se explore karna taaki hidden patterns pata chal sakein—jaise kaunsa topic sabse mushkil hai aur saal-dar-saal scores kaise badhte hain.

### Q5. How is the Financial Literacy Score calculated?
- **English**: The quiz contains 8 objective knowledge questions covering Banking, UPI Security, Compound Interest, Inflation, Loans, Investments, Risk Awareness, and Emergency Funds. Each correct answer earns 1 point. The raw score (0 to 8) is converted to a percentage:
  $$\text{Score (\%)} = \left(\frac{\text{Raw Score}}{8}\right) \times 100$$
  - **Basic**: Score $< 50\%$
  - **Intermediate**: $50\% \le \text{Score} \le 75\%$
  - **Advanced**: Score $> 75\%$

### Q6. What is Classification in Machine Learning?
- **English**: Classification is a supervised learning task where the model learns from historical labeled data to assign new, unseen observations into discrete categories. Here, the target variable is `Financial_Literacy_Level` with three classes: Basic, Intermediate, and Advanced.
- **Roman English**: Classification ek supervised ML technique hai jisme algorithm data dekh kar discrete categories (jaise Basic, Intermediate, Advanced) predict karta hai.

### Q7. Why did you choose a Decision Tree Classifier?
- **English**: We chose a Decision Tree because it provides **high explainability and interpretability**. In educational research, we need to justify to students and faculty *why* a student received a particular literacy level recommendation. Unlike "black-box" models, a Decision Tree creates transparent If-Then rules based on Gini Impurity.
- **Roman English**: Decision tree isliye choose kiya kyunki yeh bahut explainable hai. Iske rules (If-Then conditions) viva mein aur students ko aasani se dikhaye ja sakte hain ki model ne kis basis pe faisla liya.

### Q8. What is Data Leakage and how did you prevent it?
- **English**: Data leakage happens when information from outside the training dataset or information that directly determines the target is used to train the model. If we had fed the `Financial_Literacy_Score` or the exact quiz answers as features, the model would cheat and achieve 100% artificial accuracy. We prevented this by **strictly using only behavioral and demographic factors** (Year of Study, Budgeting Habit, Prior Education, Saving Habit).
- **Roman English**: Data leakage ka matlab model ko aisi information dena jisse wo cheat kar sake. Humne quiz ka numerical score input features se bilkul hata diya, sirf habits aur background use kiya.

### Q9. What is a Confusion Matrix?
- **English**: A confusion matrix is an evaluation table displaying the counts of True Positives, True Negatives, False Positives, and False Negatives across all classification categories, showing where the model made errors.
- **Roman English**: Confusion matrix ek evaluation table hai jo dikhata hai ki model ne kitne predictions sahi kiye aur kahan par confuse hokar galat class predict kar di.

### Q10. Why use both MySQL and Power BI?
- **English**:
  - **MySQL**: Provides a secure, ACID-compliant relational database to store and query student records systematically using SQL.
  - **Power BI**: Serves as an industry-standard Business Intelligence dashboard for non-technical college administrators to filter cohorts using visual slicers.

### Q11. What are the limitations of this project?
- **English**:
  1. The sample data reflects a specific cohort and may not capture regional socio-economic variations.
  2. Self-reported survey answers may suffer from optimism bias (e.g., claiming to budget regularly).
  3. The model identifies statistical correlations, not definitive causal claims.

