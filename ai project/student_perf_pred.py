import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="student_data"
)

query = "SELECT * FROM performance"
data = pd.read_sql_query(query, conn)

data['result'] = data['Performance Index'].apply(lambda x: 1 if x >= 50 else 0)

data['Extracurricular Activities'] = data['Extracurricular Activities'].map({
    'Yes': 1,
    'No': 0
})

X = data[[
    'Hours Studied',
    'Previous Scores',
    'Extracurricular Activities',
    'Sleep Hours',
    'Sample Question Papers Practiced'
]]

y = data['result']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Model Accuracy:", round(accuracy_score(y_test, predictions), 2))

print("\nEnter student details:")

hours = int(input("Hours Studied (0-10): "))
scores = int(input("Previous Scores (0-100): "))
activities = int(input("Activities (1=Yes, 0=No): "))
sleep = int(input("Sleep Hours (0-10): "))
papers = int(input("Practice Papers (0-10): "))

if not (0 <= hours <= 10 and
        0 <= scores <= 100 and
        activities in [0, 1] and
        0 <= sleep <= 10 and
        0 <= papers <= 10):
    print("Invalid input. Please enter values in correct ranges.")
    exit()

new_data = pd.DataFrame([[
    hours, scores, activities, sleep, papers
]], columns=[
    'Hours Studied',
    'Previous Scores',
    'Extracurricular Activities',
    'Sleep Hours',
    'Sample Question Papers Practiced'
])

prediction = model.predict(new_data)[0]

if prediction == 1:
    print("\nPrediction: PASS")
else:
    print("\nPrediction: FAIL")