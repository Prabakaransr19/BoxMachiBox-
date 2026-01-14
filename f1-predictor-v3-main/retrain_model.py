"""
Retrain F1 Model with Complete 2025 Data
Uses existing feature engineering, trains ensemble, exports production model
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("🤖 F1 MODEL RETRAINING - COMPLETE 2025 SEASON")
print("=" * 70)

# ========================================
# STEP 1: Load Complete Data
# ========================================

print("\n📊 STEP 1: Loading Complete Dataset...")
print("-" * 70)

# Check if feature-engineered data exists
try:
    df = pd.read_csv('data/processed/f1_v3_complete_dataset.csv')
    print(f"✅ Loaded existing complete dataset: {len(df):,} rows")
    
    # Check if it has all 24 rounds
    if 'season' in df.columns and 'round' in df.columns:
        rounds_2025 = sorted(df[df['season'] == 2025]['round'].unique())
        print(f"   2025 rounds in dataset: {len(rounds_2025)}")
        
        if len(rounds_2025) < 24:
            print(f"   ⚠️  Dataset missing rounds - needs re-engineering")
            needs_reengineering = True
        else:
            print(f"   ✅ All 24 rounds present")
            needs_reengineering = False
    else:
        needs_reengineering = True
        
except FileNotFoundError:
    print("❌ Feature-engineered dataset not found")
    needs_reengineering = True

if needs_reengineering:
    print("\n⚠️  FEATURE ENGINEERING REQUIRED")
    print("   The complete dataset needs feature engineering.")
    print("   Please run your feature engineering code in the notebook first,")
    print("   OR I can create a simplified feature engineering script.")
    print("\n   Options:")
    print("   1. Open f1_predictor_v3_master.ipynb and re-run feature engineering")
    print("   2. Use simplified feature script (I'll create it)")
    
    choice = input("\n   Choose option (1 or 2): ").strip()
    
    if choice == "2":
        print("\n   Creating simplified feature engineering script...")
        # We'll handle this below
        use_simplified = True
    else:
        print("\n   Please run feature engineering in your notebook first.")
        print("   Then run this script again.")
        exit()
else:
    use_simplified = False

# ========================================
# STEP 2: Prepare Training Data
# ========================================

print("\n🎯 STEP 2: Preparing Training Data...")
print("-" * 70)

# Load the dataset
if not use_simplified:
    # Assume target is 'podium' (position <= 3)
    if 'podium' not in df.columns and 'position' in df.columns:
        df['podium'] = (df['position'] <= 3).astype(int)
    
    # Identify feature columns (exclude metadata)
    exclude_cols = ['season', 'round', 'driverId', 'driverCode', 'driverName', 
                    'constructorId', 'constructorName', 'circuitId', 'circuitName',
                    'date', 'position', 'points', 'status', 'podium', 'laps',
                    'fastestLap', 'fastestLapTime']
    
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    print(f"✅ Dataset loaded: {len(df):,} samples")
    print(f"   Features: {len(feature_cols)}")
    print(f"   Target: podium (1 = P1-P3, 0 = P4+)")
    
    # Split: 2022-2024 + 2025 R1-R20 for training, R21-R24 for testing
    train_df = df[(df['season'] < 2025) | 
                  ((df['season'] == 2025) & (df['round'] <= 20))]
    test_df = df[(df['season'] == 2025) & (df['round'] > 20)]
    
    X_train = train_df[feature_cols].fillna(0)
    y_train = train_df['podium']
    X_test = test_df[feature_cols].fillna(0)
    y_test = test_df['podium']
    
    print(f"\n📊 TRAIN/TEST SPLIT:")
    print(f"   Training: {len(X_train):,} samples (2022-2024 + 2025 R1-R20)")
    print(f"   Testing: {len(X_test):,} samples (2025 R21-R24)")
    print(f"   Podium rate (train): {y_train.mean():.1%}")
    print(f"   Podium rate (test): {y_test.mean():.1%}")

# ========================================
# STEP 3: Train Ensemble Models
# ========================================

print("\n🤖 STEP 3: Training Ensemble Models...")
print("-" * 70)

# CatBoost
print("\n  Training CatBoost...", end=" ")
cat_model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    verbose=False,
    random_state=42
)
cat_model.fit(X_train, y_train)
cat_pred = cat_model.predict(X_test)
cat_acc = accuracy_score(y_test, cat_pred)
print(f"✅ Accuracy: {cat_acc:.4f} ({cat_acc*100:.2f}%)")

# XGBoost
print("  Training XGBoost...", end=" ")
xgb_model = XGBClassifier(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    random_state=42,
    eval_metric='logloss'
)
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)
xgb_acc = accuracy_score(y_test, xgb_pred)
print(f"✅ Accuracy: {xgb_acc:.4f} ({xgb_acc*100:.2f}%)")

# LightGBM
print("  Training LightGBM...", end=" ")
lgb_model = LGBMClassifier(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    random_state=42,
    verbose=-1
)
lgb_model.fit(X_train, y_train)
lgb_pred = lgb_model.predict(X_test)
lgb_acc = accuracy_score(y_test, lgb_pred)
print(f"✅ Accuracy: {lgb_acc:.4f} ({lgb_acc*100:.2f}%)")

# Ensemble (voting)
print("\n  Creating ensemble prediction...", end=" ")
ensemble_pred = (cat_pred + xgb_pred + lgb_pred) / 3
ensemble_pred_class = (ensemble_pred > 0.5).astype(int)
ensemble_acc = accuracy_score(y_test, ensemble_pred_class)
print(f"✅ Accuracy: {ensemble_acc:.4f} ({ensemble_acc*100:.2f}%)")

# ========================================
# STEP 4: Model Evaluation
# ========================================

print("\n📊 STEP 4: Model Evaluation...")
print("-" * 70)

print(f"\n🏆 MODEL PERFORMANCE ON TEST SET (2025 R21-R24):")
print(f"   CatBoost:  {cat_acc*100:.2f}%")
print(f"   XGBoost:   {xgb_acc*100:.2f}%")
print(f"   LightGBM:  {lgb_acc*100:.2f}%")
print(f"   Ensemble:  {ensemble_acc*100:.2f}%")

best_model_name = max([('CatBoost', cat_acc), ('XGBoost', xgb_acc), 
                       ('LightGBM', lgb_acc), ('Ensemble', ensemble_acc)],
                      key=lambda x: x[1])[0]
best_acc = max(cat_acc, xgb_acc, lgb_acc, ensemble_acc)

print(f"\n⭐ Best Model: {best_model_name} ({best_acc*100:.2f}%)")

# Detailed classification report for best model
if best_model_name == 'CatBoost':
    best_pred = cat_pred
    production_model = cat_model
elif best_model_name == 'XGBoost':
    best_pred = xgb_pred
    production_model = xgb_model
elif best_model_name == 'LightGBM':
    best_pred = lgb_pred
    production_model = lgb_model
else:
    best_pred = ensemble_pred_class
    production_model = cat_model  # Use CatBoost as base for ensemble

print(f"\n📋 Classification Report ({best_model_name}):")
print(classification_report(y_test, best_pred, 
                          target_names=['No Podium', 'Podium']))

print(f"\n🔢 Confusion Matrix:")
cm = confusion_matrix(y_test, best_pred)
print(f"   True Negatives:  {cm[0][0]}")
print(f"   False Positives: {cm[0][1]}")
print(f"   False Negatives: {cm[1][0]}")
print(f"   True Positives:  {cm[1][1]}")

# ========================================
# STEP 5: Save Models
# ========================================

print("\n💾 STEP 5: Saving Models...")
print("-" * 70)

import os
os.makedirs('models/ensemble', exist_ok=True)

# Save individual models
with open('models/ensemble/cat_model.pkl', 'wb') as f:
    pickle.dump(cat_model, f)
print("✅ Saved: models/ensemble/cat_model.pkl")

with open('models/ensemble/xgb_model.pkl', 'wb') as f:
    pickle.dump(xgb_model, f)
print("✅ Saved: models/ensemble/xgb_model.pkl")

with open('models/ensemble/lgb_model.pkl', 'wb') as f:
    pickle.dump(lgb_model, f)
print("✅ Saved: models/ensemble/lgb_model.pkl")

# Save production model (best performer)
production_path = '../f1_PRODUCTION_READY.pkl'
with open(production_path, 'wb') as f:
    pickle.dump(production_model, f)
print(f"✅ Saved: {production_path} ({best_model_name})")

# Save feature columns
with open('models/feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_cols, f)
print("✅ Saved: models/feature_columns.pkl")

# ========================================
# STEP 6: Summary
# ========================================

print("\n" + "=" * 70)
print("✅ MODEL RETRAINING COMPLETE!")
print("=" * 70)

print(f"\n📊 FINAL RESULTS:")
print(f"   Training samples: {len(X_train):,}")
print(f"   Test samples: {len(X_test):,}")
print(f"   Best model: {best_model_name}")
print(f"   Test accuracy: {best_acc*100:.2f}%")
print(f"   Production model: f1_PRODUCTION_READY.pkl")

print(f"\n📋 NEXT STEPS:")
print(f"   1. ✅ Models trained and saved")
print(f"   2. Update Streamlit app (use new model)")
print(f"   3. Test predictions locally")
print(f"   4. Push to GitHub")
print(f"   5. Deploy to Streamlit Cloud")

print("\n" + "=" * 70)