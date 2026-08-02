import pandas as pd

# ==========================
# Load cleaned dataset
# ==========================
df = pd.read_csv("data/processed/young_players.csv")

print("=" * 50)
print("WonderKid AI - Scoring")
print("=" * 50)

print(f"\nPlayers: {len(df)}")

# ==========================
# Metrics for Version 1
# ==========================
metrics = [
    "Gls",
    "Ast",
    "xG",
    "xAG",
    "PrgC",
    "PrgP",
    "KP",
    "Min"
]

# Keep only metrics that actually exist
metrics = [m for m in metrics if m in df.columns]

print("\nMetrics Used:")
print(metrics)

# ==========================
# Convert each metric into percentile
# ==========================
for metric in metrics:
    df[f"{metric}_score"] = df[metric].rank(pct=True) * 100

print("\nPercentile scores created.")

# ==========================
# WonderKid Score
# ==========================

score_columns = [f"{m}_score" for m in metrics]

df["WonderKidScore"] = df[score_columns].mean(axis=1)

print("\nWonderKid Score calculated.")

# ==========================
# Rank Players
# ==========================

df = df.sort_values(
    by="WonderKidScore",
    ascending=False
)

print("\nTop 20 WonderKids")

print(
    df[
        [
            "Player",
            "Age",
            "Pos",
            "Squad",
            "WonderKidScore"
        ]
    ]
    .head(20)
    .to_string(index=False)
)

# ==========================
# Save Rankings
# ==========================

df.to_csv(
    "data/processed/wonderkid_rankings.csv",
    index=False
)

print("\nSaved wonderkid_rankings.csv")