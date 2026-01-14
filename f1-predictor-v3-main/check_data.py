import pandas as pd
import os

print("📂 CHECKING EXISTING DATA FILES")
print("=" * 60)

# Check race results
if os.path.exists('data/raw/race_results_2022_2025.csv'):
    df = pd.read_csv('data/raw/race_results_2022_2025.csv')
    print(f"\n✅ Race Results:")
    print(f"   Rows: {len(df):,}")
    if 'season' in df.columns and 'round' in df.columns:
        rounds_2025 = sorted(df[df['season'] == 2025]['round'].unique())
        print(f"   2025 Rounds: {rounds_2025}")
        print(f"   Missing rounds: {[r for r in range(1,25) if r not in rounds_2025]}")

# Check complete dataset
if os.path.exists('data/processed/f1_v3_complete_dataset.csv'):
    df = pd.read_csv('data/processed/f1_v3_complete_dataset.csv')
    print(f"\n✅ Complete Dataset:")
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    if 'season' in df.columns and 'round' in df.columns:
        rounds_2025 = sorted(df[df['season'] == 2025]['round'].unique())
        print(f"   2025 Rounds: {rounds_2025}")