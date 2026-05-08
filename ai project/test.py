import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Make pandas output look wider and prevent column wrapping
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# 1. Load data
# This uses the CSV file verbatim as requested
data = pd.read_csv("Student_Performance.csv")

# ==============================
# PREPROCESSING & FEATURE ENGINEERING
# ==============================
# Create binary Target: 1 for Pass (Index >= 50), 0 for Fail
# We use 'result' to match your Flask app's naming convention
data['result'] = (data['Performance Index'] >= 50).astype(int)

# Convert categorical column to numeric
data['Extracurricular Activities'] = data['Extracurricular Activities'].map({'Yes': 1, 'No': 0})

print("\n" + "="*60)
print(" FIRST 5 ROWS OF DATA")
print("="*60)
print(data.head())

print("\n" + "="*60)
print(" DATA INFO")
print("="*60)
data.info()

print("\n" + "="*60)
print(" DESCRIPTIVE STATISTICS (Rounded)")
print("="*60)
print(data.describe().round(2))

# ==============================
# DATA CLEANING
# ==============================
# Treat zeros as missing values for columns where 0 is unlikely or indicates a recording error.
# Note: 'Hours Studied' and 'Papers Practiced' could genuinely be 0, so we exclude them from replacement.
columns_to_clean = ['Previous Scores', 'Sleep Hours']
data[columns_to_clean] = data[columns_to_clean].replace(0, np.nan)

# Impute missing values with the median
data.fillna(data.median(), inplace=True)

print("\n" + "="*60)
print(" MISSING VALUES AFTER CLEANING")
print("="*60)
print(data.isnull().sum())

# ==============================
# MODEL BUILDING
# ==============================
# Define features (X) and target (y)
# IMPORTANT: We drop 'result' (target) AND 'Performance Index' (the original target)
# to prevent the model from "cheating" and to match your Flask input list.
X = data.drop(['result', 'Performance Index'], axis=1)
y = data['result']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data (Prevents the 'Red Convergence Warning' and improves Logistic Regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train the Logistic Regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Make predictions
predictions = model.predict(X_test_scaled)

# ==============================
# FINAL EVALUATION
# ==============================
print("\n" + "="*60)
print(" MODEL RESULTS (GRADE GUARDIAN: PASS/FAIL PREDICTOR)")
print("="*60)
print(f"Accuracy Score: {accuracy_score(y_test, predictions) * 100:.2f}%")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions))
print("="*60 + "\n")