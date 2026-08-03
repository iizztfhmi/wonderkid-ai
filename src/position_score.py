import pandas as pd
from pathlib import Path

from config import POSITION_CONFIG

print("=" * 60)
print("WonderKid AI - Position Scoring")
print("=" * 60)

input_folder = Path("data/processed")
output_folder = Path("data/rankings")

output_folder.mkdir(parents=True, exist_ok=True)

# Metrics that should be converted to per-90
PER90_METRICS = {
    "Gls",
    "Ast",
    "xG",
    "xAG",
    "Sh",
    "SoT",
    "KP",
    "SCA",
    "GCA",
    "PrgC",
    "PrgP",
    "Carries",
    "Tkl",
    "Int",
    "Blocks",
    "Clr",
    "Won",
    "Recov",
    "Succ",
    "Touches"
}

for position, config in POSITION_CONFIG.items():

    print(f"\nScoring {position}...")

    file_path = input_folder / f"{position}.csv"

    if not file_path.exists():
        print(f"{position}.csv not found.")
        continue

    df = pd.read_csv(file_path)

    metrics = config["metrics"]
    score_columns = []

    for metric, weight in metrics.items():

        if metric not in df.columns:
            print(f"Missing column: {metric}")
            continue

        values = df[metric].fillna(0)

        # Convert only counting statistics to per-90
        if metric in PER90_METRICS:
            values = values / df["90s"].replace(0, 1)

        # Min-Max Normalization
        min_value = values.min()
        max_value = values.max()

        if max_value == min_value:
            normalized = pd.Series(50, index=df.index)
        else:
            normalized = ((values - min_value) / (max_value - min_value)) * 100

        column_name = f"{metric}_Score"

        df[column_name] = normalized
        score_columns.append((column_name, weight))

    score_name = f"{position}_Score"

    df[score_name] = 0.0

    for column, weight in score_columns:
        df[score_name] += df[column] * weight

    df = df.sort_values(score_name, ascending=False)

    output_file = output_folder / f"{position}_rankings.csv"
    df.to_csv(output_file, index=False)

    print(df[["Player", score_name]].head())

print("\nDone!")