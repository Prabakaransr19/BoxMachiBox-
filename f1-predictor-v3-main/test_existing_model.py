"""
Test Existing CatBoost Model with Complete 2025 Data
"""

import pandas as pd
import pickle
import numpy as np
from sklearn.metrics import accuracy_score

print("=" * 70)
print("🧪 TESTING EXISTING MODEL WITH COMPLETE 2025 DATA")
print("=" * 70)

# Load existing CatBoost model
print("\n📦 Loading existing CatBoost model...")
with open('models/ensemble/xgb_model.pkl', 'rb') as f:
    cat_model = pickle.load(f)  # Keep variable name same

print("✅ Model loaded successfully")

# Load complete dataset
print("\n📊 Loading complete dataset...")
df = pd.read_csv('data/processed/f1_v3_complete_dataset.csv')
print(f"✅ Dataset loaded: {len(df):,} rows")

# Check 2025 coverage
rounds_2025 = sorted(df[df['season'] == 2025]['round'].unique())
print(f"   2025 rounds: {len(rounds_2025)} (R{min(rounds_2025)}-R{max(rounds_2025)})")

# Prepare data
if 'podium' not in df.columns and 'position' in df.columns:
    df['podium'] = (df['position'] <= 3).astype(int)

# Identify features
exclude_cols = ['season', 'round', 'driverId', 'driverCode', 'driverName', 
                'constructorId', 'constructorName', 'circuitId', 'circuitName',
                'date', 'position', 'points', 'status', 'podium', 'laps',
                'fastestLap', 'fastestLapTime']
feature_cols = [col for col in df.columns if col not in exclude_cols]

# Test on 2025 R20-R24
test_df = df[(df['season'] == 2025) & (df['round'] >= 20)]
X_test = test_df[feature_cols].fillna(0)
y_test = test_df['podium']

print(f"\n🎯 Testing on 2025 R20-R24...")
print(f"   Test samples: {len(X_test)}")

# Predict
y_pred = cat_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n📊 RESULTS:")
print(f"   Accuracy: {accuracy*100:.2f}%")
print(f"   Model is {'✅ READY' if accuracy > 0.85 else '⚠️  NEEDS RETRAINING'}")

print("\n" + "=" * 70)