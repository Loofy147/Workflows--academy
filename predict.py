# predict.py
import sys
import argparse
import joblib

# Load the model
model = joblib.load("predictor.joblib")

# Parse the input
parser = argparse.ArgumentParser(description="Predict workflow success or failure.")
parser.add_argument("duration", type=int, help="The duration of the workflow run in seconds.")
args = parser.parse_args()

# Make a prediction
prediction = model.predict([[args.duration]])[0]

# Output the prediction
if prediction == 1:
    print("success")
else:
    print("failure")
