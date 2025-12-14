# validate_data.py
import sys
import pandas as pd

df = pd.read_csv("workflow_runs.csv")

if df["run_id"].isnull().any():
    print("Error: run_id column contains null values.")
    sys.exit(1)

if not df["status"].isin(["success", "failure"]).all():
    print("Error: status column contains invalid values.")
    sys.exit(1)

print("Data validation successful.")
