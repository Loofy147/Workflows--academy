import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv('workflow_runs.csv')

# Preprocess the data
df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
df = df.dropna(subset=['duration_seconds', 'status'])
df['status'] = df['status'].apply(lambda x: 1 if x == 'success' else 0)

# Select features and labels
features = ['duration_seconds']
labels = 'status'

X = df[features]
y = df[labels]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")

# Save the trained model
joblib.dump(model, 'predictor.joblib')

print("Model trained and saved to predictor.joblib")
