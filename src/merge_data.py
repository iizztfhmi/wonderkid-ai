import pandas as pd

print("=" * 60)
print("WonderKid AI - Merge Dataset")
print("=" * 60)

# Load datasets
stats = pd.read_csv("data/processed/young_players.csv")
metadata = pd.read_csv("data/metadata/player_metadata.csv")

print(f"Stats dataset    : {stats.shape}")
print(f"Metadata dataset : {metadata.shape}")

# Merge
merged = stats.merge(
    metadata,
    on="Player",
    how="left"
)

print(f"Merged dataset   : {merged.shape}")

# Check missing metadata
missing = merged[merged["Club"].isna()]

print("\nMissing Metadata:")
print(missing["Player"].tolist())

# Save
merged.to_csv(
    "data/processed/wonderkid_dataset.csv",
    index=False
)

print("\nSaved:")
print("data/processed/wonderkid_dataset.csv")