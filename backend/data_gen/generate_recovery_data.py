import pandas as pd
import numpy as np
np.random.seed(42)
n = 2500

data = {
    'age': np.random.randint(18, 81, n),
    'sex': np.random.choice(['Male', 'Female'], n, p=[0.5, 0.5]),
    'weight': np.random.normal(75, 15, n).astype(int).clip(40, 150),
    'height': np.random.normal(170, 10, n).astype(int).clip(140, 200),
    'condition_type': np.random.choice(['Cold', 'Flu', 'Fever', 'Headache', 'Cough', 'Sore Throat', 'Stomach Ache'], n),
    'severity_score': np.random.randint(1, 11, n),
    'diabetic': np.random.binomial(1, 0.12, n),
    'exercise': np.random.binomial(1, 0.65, n),
    'alcohol_units': np.random.poisson(5, n).clip(0, 30),
    'sleep_hours': np.random.normal(7, 1.2, n).clip(3, 12),
    'medication_adherence': np.random.normal(0.75, 0.2, n).clip(0,1),
    'smoking_status': np.random.choice(['Never', 'Former', 'Current'], n, p=[0.6, 0.25, 0.15]),
}
df = pd.DataFrame(data)

# Realistic target (base + lifestyle factors + noise) → NOT overly optimistic
base = (4 + df['severity_score'] * 1.5 +
        (df['age'] > 60) * 4 +
        df['diabetic'] * 3 +
        (1 - df['exercise']) * 2.5 +
        (df['alcohol_units'] > 10) * 1.5 +
        (df['sleep_hours'] < 6) * 3.5 +
        (df['smoking_status'] == 'Current') * 4 +
        (df['medication_adherence'] < 0.5) * 2)
df['recovery_days'] = (base + np.random.normal(0, 2.5, n)).clip(1, 35).astype(int)

df.to_csv('backend/data_gen/recovery_data.csv', index=False)
print("Recovery dataset saved (2500 rows). Sample recovery_days mean:", df['recovery_days'].mean())