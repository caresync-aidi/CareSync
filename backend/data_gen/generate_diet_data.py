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
    'diabetic': np.random.binomial(1, 0.12, n),
    'exercise': np.random.binomial(1, 0.65, n),
    'alcohol_units': np.random.poisson(5, n).clip(0, 30),
    'daily_steps': np.random.normal(8000, 3000, n).astype(int).clip(2000, 20000),
    'sleep_hours': np.random.normal(7, 1.2, n).clip(3, 12),
}
df = pd.DataFrame(data)
df['bmi'] = df['weight'] / (df['height']/100)**2

# Realistic diet_plan based on conditions + lifestyle (with 20% noise)
def get_diet(row):
    if row['diabetic'] == 1:
        return 'Low-Carb Diet'
    if row['condition_type'] in ['Flu', 'Cold', 'Fever', 'Stomach Ache']:
        return 'Balanced Diet'
    if row['condition_type'] in ['Headache', 'Cough', 'Sore Throat']:
        return 'Anti-Inflammatory Diet'
    if row['exercise'] == 1 and row['daily_steps'] > 10000:
        return 'High-Protein Diet'
    return np.random.choice(['Balanced Diet', 'Low-Carb Diet', 'High-Protein Diet', 'Anti-Inflammatory Diet', 'Low-Sodium Diet'])

df['diet_plan'] = df.apply(get_diet, axis=1)
# Add noise
mask = np.random.rand(n) < 0.2
df.loc[mask, 'diet_plan'] = np.random.choice(['Balanced Diet', 'Low-Carb Diet', 'High-Protein Diet', 'Anti-Inflammatory Diet', 'Low-Sodium Diet'], mask.sum())

df.to_csv('backend/data_gen/diet_data.csv', index=False)
print("Diet dataset saved. Diet plan distribution:\n", df['diet_plan'].value_counts())