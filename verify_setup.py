"""
Financial Literacy Project - Environment Verification Script
Run this script to confirm your Python environment is ready.
"""

import sys

def check_environment():
    print("=" * 60)
    print("   FINANCIAL LITERACY PROJECT - ENVIRONMENT CHECK")
    print("=" * 60)
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version   : {sys.version.split()[0]}")
    print("-" * 60)

    packages = {
        "flask": "Flask (Web Framework)",
        "pandas": "Pandas (Data Manipulation)",
        "numpy": "NumPy (Numerical Computing)",
        "matplotlib": "Matplotlib (Data Visualization)",
        "seaborn": "Seaborn (Statistical Charts)",
        "sklearn": "Scikit-learn (Machine Learning)",
        "mysql.connector": "MySQL Connector (Database)",
        "openpyxl": "OpenPyXL (Excel Integration)",
        "joblib": "Joblib (Model Persistence)"
    }

    all_passed = True
    for module_name, display_name in packages.items():
        try:
            mod = __import__(module_name)
            ver = getattr(mod, "__version__", "installed")
            print(f"[OK] {display_name:<32} (v{ver})")
        except ImportError:
            print(f"[MISSING] {display_name:<28} -> Please install via requirements.txt")
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("SUCCESS: All required libraries are installed and ready!")
        print("You can proceed to Step 2 (Dataset Creation & Survey Logic).")
    else:
        print("ACTION REQUIRED: Run 'pip install -r requirements.txt' in your terminal.")
    print("=" * 60)

if __name__ == "__main__":
    check_environment()

