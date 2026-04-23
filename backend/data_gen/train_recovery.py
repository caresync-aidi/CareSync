import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib

df = pd.read_csv('backend/data_gen/recovery_data.csv')
categorical = ['sex', 'condition_type', 'smoking_status']
numeric = ['age', 'weight', 'height', 'severity_score', 'diabetic', 'exercise', 'alcohol_units', 'sleep_hours', 'medication_adherence']

X = df[categorical + numeric]
y = df['recovery_days']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical),
    ('num', 'passthrough', numeric)
])

pipeline = Pipeline([('preprocessor', preprocessor), ('model', RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42))])
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(f"Recovery Model - MAE: {mean_absolute_error(y_test, y_pred):.2f} days | R²: {r2_score(y_test, y_pred):.2f} (realistic)")
joblib.dump(pipeline, 'backend/models/model_recovery.joblib')
print("Recovery model saved")