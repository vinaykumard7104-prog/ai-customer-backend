"""
Train the customer churn prediction model.
Run this once: python train_model.py
The saved model.pkl is loaded automatically by app.py
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Expanded training dataset
data = {
    "time_spent": [5, 10, 2, 15, 7, 12, 3, 20, 1, 18, 6, 9, 4, 25, 8, 11, 2, 30, 5, 14],
    "clicks":     [10, 25, 5, 40, 15, 30, 7, 50, 3, 45, 12, 22, 8, 60, 18, 28, 4, 70, 9, 35],
    "pages":      [3,  5,  1,  8,  4,  6,  2, 10, 1,  9,  3,  5, 2, 12,  4,  7, 1, 15, 2,  7],
    "churn":      [0,  0,  1,  0,  0,  0,  1,  0, 1,  0,  0,  0, 1,  0,  0,  0, 1,  0, 1,  0]
}

df = pd.DataFrame(data)

X = df[["time_spent", "clicks", "pages"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, zero_division=0))

# Save model
joblib.dump(model, "model.pkl")
print("Model saved to model.pkl")
