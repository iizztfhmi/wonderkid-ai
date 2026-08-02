import pandas as pd

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("data/raw/players_data-2025_2026.csv")

print("=" * 50)
print("WonderKid AI - Preprocessing")
print("=" * 50)

print(f"\nOriginal dataset: {df.shape}")

# ==========================
# Filter Age (16-21)
# ==========================
young_players = df[
    (df["Age"] >= 16) &
    (df["Age"] <= 21)
]

print(f"\nPlayers aged 16-21: {young_players.shape}")

# ==========================
# Minimum Minutes Played
# ==========================
MINIMUM_MINUTES = 360

young_players = young_players[
    young_players["Min"] >= MINIMUM_MINUTES
]

print(f"\nPlayers with at least {MINIMUM_MINUTES} minutes: {young_players.shape}")

# ==========================
# Remove Goalkeepers
# ==========================
young_players = young_players[
    ~young_players["Pos"].str.contains("GK", na=False)
]

print(f"\nAfter removing goalkeepers: {young_players.shape}")

# ==========================
# Position Breakdown
# ==========================
print("\nPosition Breakdown:")
print(young_players["Pos"].value_counts())

# ==========================
# Split By Position
# ==========================
forwards = young_players[
    young_players["Pos"].str.contains("FW", na=False)
]

midfielders = young_players[
    young_players["Pos"].str.contains("MF", na=False)
]

defenders = young_players[
    young_players["Pos"].str.contains("DF", na=False)
]

print("\nPosition Groups")
print("----------------")
print(f"Forwards     : {len(forwards)}")
print(f"Midfielders  : {len(midfielders)}")
print(f"Defenders    : {len(defenders)}")

# ==========================
# Preview Dataset
# ==========================
print("\nTop 10 Players")

preview_columns = [
    "Player",
    "Age",
    "Pos",
    "Squad",
    "Comp",
    "Min",
    "Gls",
    "Ast",
    "xG",
    "xAG"
]

print(
    young_players[preview_columns]
    .head(10)
    .to_string(index=False)
)

# ==========================
# Save Clean Dataset
# ==========================
young_players.to_csv(
    "data/processed/young_players.csv",
    index=False
)

forwards.to_csv(
    "data/processed/forwards.csv",
    index=False
)

midfielders.to_csv(
    "data/processed/midfielders.csv",
    index=False
)

defenders.to_csv(
    "data/processed/defenders.csv",
    index=False
)

print("\nDatasets saved successfully!")

print("""
Generated Files:
----------------
data/processed/
├── young_players.csv
├── forwards.csv
├── midfielders.csv
└── defenders.csv
""")