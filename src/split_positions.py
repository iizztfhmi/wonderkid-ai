import pandas as pd
from pathlib import Path

print("=" * 60)
print("WonderKid AI - Position Split")
print("=" * 60)

# Load dataset
df = pd.read_csv("data/processed/wonderkid_dataset.csv")

print(f"\nPlayers loaded: {len(df)}")

# Positions to create
POSITIONS = [
    "ST",
    "LW",
    "RW",
    "CAM",
    "CM",
    "CDM",
    "LB",
    "CB",
    "RB"
]

# Output folder
output_folder = Path("data/processed")
output_folder.mkdir(exist_ok=True)

print("\nSplitting players...\n")

# Create one dataset for each position
for position in POSITIONS:

    position_df = df[
        (df["PrimaryPosition"] == position) |
        (df["SecondaryPosition"] == position) |
        (df["ThirdPosition"] == position)
    ]

    position_df.to_csv(
        output_folder / f"{position}.csv",
        index=False
    )

    print(f"{position:<4}: {len(position_df):>2} players")

print("\nDatasets created successfully!")

print("\nGenerated Files")
print("-" * 20)

for position in POSITIONS:
    print(f"{position}.csv")