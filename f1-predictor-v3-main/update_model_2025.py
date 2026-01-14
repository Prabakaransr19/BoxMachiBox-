"""
F1 Model Update Script - Add 2025 R20-R24 Data
Fetches missing races, retrains model, exports production file
"""

import pandas as pd
import numpy as np
import fastf1
from datetime import datetime
import pickle
import warnings
import os
warnings.filterwarnings('ignore')

print("=" * 70)
print("🏎️  F1 MODEL UPDATE - 2025 COMPLETE SEASON")
print("=" * 70)

# Create and enable FastF1 cache
os.makedirs('f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('f1_cache')
print("✅ Cache directory created")

# ========================================
# STEP 1: Fetch Missing 2025 Races (R20-R24)
# ========================================

print("\n📡 STEP 1: Fetching 2025 R20-R24 Data...")
print("-" * 70)

missing_rounds = [20, 21, 22, 23, 24]
new_race_results = []

for round_num in missing_rounds:
    try:
        print(f"\n  Fetching Round {round_num}...", end=" ")
        
        session = fastf1.get_session(2025, round_num, 'R')
        session.load()
        
        race_info = session.event
        results = session.results
        
        for idx, row in results.iterrows():
            # Match your existing data structure
            race_entry = {
                'season': 2025,
                'round': round_num,
                'circuitId': race_info.get('Location', f'circuit_{round_num}'),
                'circuitName': race_info['EventName'],
                'date': race_info['EventDate'].strftime('%Y-%m-%d') if hasattr(race_info['EventDate'], 'strftime') else str(race_info['EventDate']),
                'driverId': row['Abbreviation'].lower(),
                'driverCode': row['Abbreviation'],
                'driverName': f"{row['FirstName']} {row['LastName']}",
                'constructorId': row['TeamName'].lower().replace(' ', '_'),
                'constructorName': row['TeamName'],
                'grid': int(row['GridPosition']) if pd.notna(row['GridPosition']) else 20,
                'position': int(row['Position']) if pd.notna(row['Position']) else 20,
                'points': float(row['Points']) if pd.notna(row['Points']) else 0.0,
                'laps': int(row.get('Laps', 0)),
                'status': row['Status'],
                'fastestLap': row.get('FastestLap', None),
                'fastestLapTime': str(row.get('FastestLapTime', '')) if pd.notna(row.get('FastestLapTime')) else None,
            }
            new_race_results.append(race_entry)
        
        print(f"✅ {race_info['EventName']} - {len(results)} drivers")
        
    except Exception as e:
        print(f"⚠️  Error: {e}")
        continue

new_race_df = pd.DataFrame(new_race_results)
print(f"\n✅ Fetched {len(new_race_df)} new results from {len(new_race_df['round'].unique())} races")

# Save new data
new_race_df.to_csv('data/raw/race_results_2025_R20_R24_NEW.csv', index=False)
print(f"💾 Saved: data/raw/race_results_2025_R20_R24_NEW.csv")

# ========================================
# STEP 2: Fetch Qualifying Data (R20-R24)
# ========================================

print("\n📡 STEP 2: Fetching Qualifying Data R20-R24...")
print("-" * 70)

new_quali_results = []

for round_num in missing_rounds:
    try:
        print(f"\n  Fetching Round {round_num} qualifying...", end=" ")
        
        session = fastf1.get_session(2025, round_num, 'Q')
        session.load()
        
        race_info = session.event
        results = session.results
        
        for idx, row in results.iterrows():
            quali_entry = {
                'season': 2025,
                'round': round_num,
                'circuitName': race_info['EventName'],
                'driverId': row['Abbreviation'].lower(),
                'driverCode': row['Abbreviation'],
                'Abbreviation': row['Abbreviation'],
                'Position': int(row['Position']) if pd.notna(row['Position']) else 20,
                'Q1': row.get('Q1', pd.NaT),
                'Q2': row.get('Q2', pd.NaT),
                'Q3': row.get('Q3', pd.NaT),
            }
            new_quali_results.append(quali_entry)
        
        print(f"✅ {race_info['EventName']}")
        
    except Exception as e:
        print(f"⚠️  Error: {e}")
        continue

new_quali_df = pd.DataFrame(new_quali_results)
print(f"\n✅ Fetched {len(new_quali_df)} qualifying results")

# Save
new_quali_df.to_csv('data/raw/qualifying_results_2025_R20_R24_NEW.csv', index=False)
print(f"💾 Saved: data/raw/qualifying_results_2025_R20_R24_NEW.csv")

# ========================================
# STEP 3: Merge with Existing Data
# ========================================

print("\n🔗 STEP 3: Merging with Existing Data...")
print("-" * 70)

# Load existing
old_race_df = pd.read_csv('data/raw/race_results_2022_2025.csv')
old_quali_df = pd.read_csv('data/raw/qualifying_results_2022_2025.csv')

print(f"\nOLD DATA:")
print(f"  Race results: {len(old_race_df):,} entries")
print(f"  2025 rounds: {sorted(old_race_df[old_race_df['season']==2025]['round'].unique())}")

print(f"\nNEW DATA:")
print(f"  Race results: {len(new_race_df):,} entries")
print(f"  New rounds: {sorted(new_race_df['round'].unique())}")

# Combine
complete_race_df = pd.concat([old_race_df, new_race_df], ignore_index=True)
complete_race_df = complete_race_df.drop_duplicates(subset=['season', 'round', 'driverCode'], keep='last')

complete_quali_df = pd.concat([old_quali_df, new_quali_df], ignore_index=True)
complete_quali_df = complete_quali_df.drop_duplicates(subset=['season', 'round', 'driverCode'], keep='last')

rounds_2025 = sorted(complete_race_df[complete_race_df['season']==2025]['round'].unique())

print(f"\n✅ MERGED DATA:")
print(f"  Total race results: {len(complete_race_df):,}")
print(f"  2025 rounds: {rounds_2025}")
print(f"  Coverage: R1-R{max(rounds_2025)}")
print(f"  Total qualifying: {len(complete_quali_df):,}")

# Save complete datasets
complete_race_df.to_csv('data/raw/race_results_2022_2025_COMPLETE.csv', index=False)
complete_quali_df.to_csv('data/raw/qualifying_results_2022_2025_COMPLETE.csv', index=False)

print(f"\n💾 SAVED COMPLETE DATASETS:")
print(f"  ✅ data/raw/race_results_2022_2025_COMPLETE.csv")
print(f"  ✅ data/raw/qualifying_results_2022_2025_COMPLETE.csv")

# ========================================
# STEP 4: Summary
# ========================================

print("\n" + "=" * 70)
print("✅ DATA UPDATE COMPLETE!")
print("=" * 70)
print(f"\n📊 FINAL DATASET:")
print(f"  • Seasons: 2022-2025")
print(f"  • 2025 Rounds: {len(rounds_2025)} races (R1-R{max(rounds_2025)})")
print(f"  • Total samples: {len(complete_race_df):,}")
print(f"  • Ready for retraining: ✅")

print(f"\n📋 NEXT STEPS:")
print(f"  1. Run your feature engineering code on the complete data")
print(f"  2. Retrain your CatBoost ensemble")
print(f"  3. Validate accuracy on holdout set")
print(f"  4. Export new f1_PRODUCTION_READY.pkl")
print(f"  5. Update Streamlit deployment")

print("\n" + "=" * 70)