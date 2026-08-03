"""
WonderKid AI
Shared scouting logic used across pages.

This mirrors the report logic from scouting_report.py, refactored into
reusable functions. The original script runs input() at import time, so
it can't be imported directly into a Streamlit page — this module is the
version other files (this page, future pages, even the CLI script) can
safely import.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from config import POSITION_CONFIG

RANKING_FOLDER = Path("data/rankings")

POSITIONS = ["ST", "LW", "RW", "CAM", "CM", "CDM", "LB", "RB", "CB"]

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


@st.cache_data
def load_all_rankings():
    """Load every *_rankings.csv into a dict: {position: DataFrame}."""

    rankings = {}

    if RANKING_FOLDER.exists():
        for file in RANKING_FOLDER.glob("*_rankings.csv"):
            position = file.stem.replace("_rankings", "")
            rankings[position] = pd.read_csv(file)

    return rankings


def potential_label(score: float) -> str:
    if score >= 90:
        return "⭐⭐⭐⭐⭐ Elite Wonderkid"
    elif score >= 80:
        return "⭐⭐⭐⭐ Excellent Prospect"
    elif score >= 70:
        return "⭐⭐⭐ High Potential"
    elif score >= 60:
        return "⭐⭐ Promising Prospect"
    return "⭐ Development Player"


def recommendation_label(score: float) -> str:
    if score >= 90:
        return "★★★★★ First Team Ready"
    elif score >= 80:
        return "★★★★☆ Rotation Player"
    elif score >= 70:
        return "★★★☆☆ High Potential Prospect"
    elif score >= 60:
        return "★★☆☆☆ Development Project"
    return "★☆☆☆☆ Long-Term Project"


def build_leaderboard(rankings: dict) -> pd.DataFrame:
    """Combine every position's rankings into one board, sorted by score."""

    rows = []

    for position, df in rankings.items():

        score_col = f"{position}_Score"

        if score_col not in df.columns:
            continue

        board = df.copy()
        board["Position"] = position
        board["Score"] = board[score_col].astype(float)
        board["Rank"] = board["Score"].rank(ascending=False, method="min").astype(int)
        board["Total"] = len(board)

        keep = ["Player", "Club", "Nationality", "Age_y", "Position", "Score", "Rank", "Total"]
        rows.append(board[keep])

    if not rows:
        return pd.DataFrame(
            columns=["Player", "Club", "Nationality", "Age_y", "Position", "Score", "Rank", "Total"]
        )

    combined = pd.concat(rows, ignore_index=True)
    combined = combined.sort_values("Score", ascending=False).reset_index(drop=True)
    combined.insert(0, "Overall Rank", combined.index + 1)

    return combined


def get_player_report(rankings: dict, player: str, position: str):
    """Rebuild the full scouting report for one player in one position."""

    df = rankings.get(position)

    if df is None:
        return None

    match = df[df["Player"].str.lower() == player.lower()]

    if match.empty:
        return None

    row = match.iloc[0]
    score_col = f"{position}_Score"
    score = float(row[score_col])

    rank = int(
        df[score_col].rank(ascending=False, method="min").loc[match.index[0]]
    )
    total = len(df)

    metric_keys = POSITION_CONFIG[position]["metrics"]
    metrics = {
        METRIC_NAMES.get(m, m): row[m]
        for m in metric_keys
        if m in row.index
    }

    return {
        "player": row["Player"],
        "club": row["Club"],
        "nationality": row["Nationality"],
        "age": row["Age_y"],
        "height": row.get("Height_cm"),
        "position": position,
        "primary": row.get("PrimaryPosition", position),
        "secondary": row.get("SecondaryPosition", "-"),
        "third": row.get("ThirdPosition", "-"),
        "score": score,
        "rank": rank,
        "total": total,
        "profile_summary": POSITION_SUMMARY.get(position, ""),
        "metrics": metrics,
        "potential": potential_label(score),
        "recommendation": recommendation_label(score),
    }