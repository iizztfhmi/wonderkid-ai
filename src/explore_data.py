import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/players_data-2025_2026.csv")

print("=" * 50)
print("WonderKid AI - Dataset Explorer")
print("=" * 50)

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Players:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nData Types:")
print(df.dtypes)