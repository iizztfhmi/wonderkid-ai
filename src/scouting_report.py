import pandas as pd
from pathlib import Path

from config import POSITION_CONFIG

print("=" * 60)
print("WonderKid AI - Scouting Report")
print("=" * 60)

player_name = input("Enter player name: ").strip()

ranking_folder = Path("data/rankings")

found = False

# --------------------------------------------------
# Position Profile Descriptions
# --------------------------------------------------

POSITION_SUMMARY = {
    "ST": "Clinical striker with strong finishing, intelligent movement and goal-scoring instinct.",
    "LW": "Direct winger who creates danger through dribbling and progressive carries.",
    "RW": "Creative wide attacker capable of progressing the ball and creating chances.",
    "CAM": "Creative attacking midfielder with excellent vision, progressive passing and chance creation.",
    "CM": "Complete midfielder with strong passing, ball progression and composure.",
    "CDM": "Defensive midfielder who protects the back line through tackles and interceptions.",
    "LB": "Modern attacking full-back contributing both offensively and defensively.",
    "RB": "Energetic full-back providing width, overlaps and defensive stability.",
    "CB": "Ball-playing centre-back with strong positioning and defensive awareness."
}

# --------------------------------------------------
# Friendly Metric Names
# --------------------------------------------------

METRIC_NAMES = {
    "Gls": "Goals",
    "Ast": "Assists",
    "xG": "Expected Goals (xG)",
    "xA": "Expected Assists (xA)",
    "KP": "Key Passes",
    "PrgP": "Progressive Passes",
    "PrgC": "Progressive Carries",
    "PrgR": "Progressive Receptions",
    "Sh": "Shots",
    "SoT": "Shots on Target",
    "SCA": "Shot Creating Actions",
    "GCA": "Goal Creating Actions",
    "Carries": "Carries",
    "Cmp%": "Pass Completion %",
    "Tkl": "Tackles",
    "Int": "Interceptions",
    "Blocks": "Blocks",
    "Clr": "Clearances",
    "Recov": "Recoveries",
    "Won": "Aerial Duels Won",
    "Succ": "Successful Dribbles",
    "Crs": "Crosses"
}

# --------------------------------------------------

for file in ranking_folder.glob("*_rankings.csv"):

    df = pd.read_csv(file)

    result = df[df["Player"].str.lower() == player_name.lower()]

    if result.empty:
        continue

    row = result.iloc[0]

    position = file.stem.replace("_rankings", "")
    score_column = position + "_Score"

    score = float(row[score_column])

    # -----------------------------------------
    # Position Ranking
    # -----------------------------------------

    rank = (
        df[score_column]
        .rank(ascending=False, method="min")
        .loc[result.index[0]]
    )

    total_players = len(df)

    # -----------------------------------------
    # Potential
    # -----------------------------------------

    if score >= 90:
        potential = "⭐⭐⭐⭐⭐ Elite Wonderkid"
    elif score >= 80:
        potential = "⭐⭐⭐⭐ Excellent Prospect"
    elif score >= 70:
        potential = "⭐⭐⭐ High Potential"
    elif score >= 60:
        potential = "⭐⭐ Promising Prospect"
    else:
        potential = "⭐ Development Player"

    # -----------------------------------------
    # Recommendation
    # -----------------------------------------

    if score >= 90:
        recommendation = "★★★★★ First Team Ready"

    elif score >= 80:
        recommendation = "★★★★☆ Rotation Player"

    elif score >= 70:
        recommendation = "★★★☆☆ High Potential Prospect"

    elif score >= 60:
        recommendation = "★★☆☆☆ Development Project"

    else:
        recommendation = "★☆☆☆☆ Long-Term Project"

    # -----------------------------------------
    # Report
    # -----------------------------------------

    print("\n" + "=" * 60)
    print("SCOUTING REPORT")
    print("=" * 60)

    print("\nPlayer")
    print("-" * 30)
    print(row["Player"])

    print("\nClub")
    print("-" * 30)
    print(row["Club"])

    print("\nNationality")
    print("-" * 30)
    print(row["Nationality"])

    print("\nAge")
    print("-" * 30)
    print(row["Age_y"])

    print("\nHeight")
    print("-" * 30)
    print(f"{row['Height_cm']} cm")

    print("\nBest Position")
    print("-" * 30)
    print(position)

    print("\nWonderKid Score")
    print("-" * 30)
    print(f"{score:.2f} / 100")

    print("\nPosition Ranking")
    print("-" * 30)
    print(f"{int(rank)} / {total_players} {position}s")

    print("\nPositions")
    print("-" * 30)
    print(f"Primary   : {row['PrimaryPosition']}")
    print(f"Secondary : {row['SecondaryPosition']}")
    print(f"Third     : {row['ThirdPosition']}")

    print("\nProfile Summary")
    print("-" * 30)
    print(POSITION_SUMMARY[position])

    print("\nTop Metrics")
    print("-" * 30)

    metrics = POSITION_CONFIG[position]["metrics"]

    for metric in metrics.keys():

        if metric in row.index:

            print(
                f"{METRIC_NAMES.get(metric, metric):<30}"
                f"{row[metric]}"
            )

    print("\nRecommendation")
    print("-" * 30)
    print(recommendation)

    print("\nPotential")
    print("-" * 30)
    print(potential)

    found = True
    break

# --------------------------------------------------

if not found:
    print("\nPlayer not found.")