import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib

df = pd.read_csv('backend/data_gen/diet_data.csv')
categorical = ['sex', 'condition_type']
numeric = ['age', 'bmi', 'diabetic', 'exercise', 'alcohol_units', 'daily_steps', 'sleep_hours']

X = df[categorical + numeric]
y = df['diet_plan']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical),
    ('num', 'passthrough', numeric)
])

pipeline = Pipeline([('preprocessor', preprocessor), ('model', GradientBoostingClassifier(n_estimators=120, learning_rate=0.1, max_depth=5, random_state=42))])
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(f"Diet Model - Accuracy: {accuracy_score(y_test, y_pred):.2%} (realistic)")
joblib.dump(pipeline, 'backend/models/model_diet.joblib')
print("Diet model saved")