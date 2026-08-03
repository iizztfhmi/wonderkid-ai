import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# ==========================================================
# Import AI Projection Module
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR / "src") not in sys.path:
    sys.path.append(str(ROOT_DIR / "src"))

from ai_projection import generate_projection
from config import POSITION_CONFIG


# ==========================================================
# Page Title
# ==========================================================

st.title("AI Future Projection")
st.caption("Predict the future career path of a WonderKid using Gemini AI.")


# ==========================================================
# Load Ranking Data
# ==========================================================

@st.cache_data
def load_players():

    ranking_folder = ROOT_DIR / "data" / "rankings"

    all_players = []

    for file in ranking_folder.glob("*_rankings.csv"):

        position = file.stem.replace("_rankings", "")

        df = pd.read_csv(file)

        score_column = f"{position}_Score"

        if score_column not in df.columns:
            continue

        df["BestPosition"] = position
        df["WonderKidScore"] = df[score_column]

        all_players.append(df)

    players = pd.concat(all_players, ignore_index=True)

    players = (
        players
        .sort_values("WonderKidScore", ascending=False)
        .drop_duplicates(subset="Player", keep="first")
        .reset_index(drop=True)
    )

    return players


players = load_players()


# ==========================================================
# Helper Functions
# ==========================================================

def get_player(player_name):

    row = players[
        players["Player"] == player_name
    ]

    if row.empty:
        return None

    return row.iloc[0]


def get_position_metrics(player):

    position = player["BestPosition"]

    metrics = {}

    if position not in POSITION_CONFIG:
        return metrics

    for metric in POSITION_CONFIG[position]["metrics"]:

        if metric in player.index:
            value = player[metric]

            if pd.notna(value):
                metrics[metric] = value

    return metrics


def get_player_rank(player):

    position = player["BestPosition"]

    ranking_file = (
        ROOT_DIR /
        "data" /
        "rankings" /
        f"{position}_rankings.csv"
    )

    ranking_df = pd.read_csv(ranking_file)

    score_column = f"{position}_Score"

    ranking_df = ranking_df.sort_values(
        score_column,
        ascending=False
    ).reset_index(drop=True)

    rank = (
        ranking_df.index[
            ranking_df["Player"] == player["Player"]
        ][0]
        + 1
    )

    total = len(ranking_df)

    return rank, total


# ==========================================================
# Player Selection
# ==========================================================

player_name = st.selectbox(
    "Select a WonderKid",
    sorted(players["Player"].unique())
)

player = get_player(player_name)

if player is None:
    st.stop()

# ==========================================================
# Player Information
# ==========================================================

rank, total = get_player_rank(player)
metrics = get_position_metrics(player)

st.divider()

st.subheader(f"👤 {player['Player']}")

# Top Information Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🏟 Club",
        player["Club"]
    )

    st.metric(
        "🌍 Nationality",
        player["Nationality"]
    )

with col2:
    st.metric(
        "🎂 Age",
        int(player["Age_y"])
    )

    st.metric(
        "📏 Height",
        f"{int(player['Height_cm'])} cm"
    )

with col3:
    st.metric(
        "⚽ Position",
        player["BestPosition"]
    )

    st.metric(
        "⭐ WonderKid Score",
        f"{player['WonderKidScore']:.1f}"
    )

st.success(
    f"Position Ranking: #{rank} of {total} {player['BestPosition']} players"
)

st.divider()
# ==========================================================
# Generate Button
# ==========================================================

generate = st.button(
    "🤖 Generate AI Projection",
    type="primary",
    use_container_width=True,
)
# ==========================================================
# Generate AI Projection
# ==========================================================

if generate:

    with st.spinner("Analyzing player profile with Gemini AI..."):

        try:

            projection = generate_projection({

                "player": player["Player"],

                "club": player["Club"],

                "age": int(player["Age_y"]),

                "nationality": player["Nationality"],

                "position": player["BestPosition"],

                "score": float(player["WonderKidScore"]),

                "rank": rank,

                "total": total,

                "metrics": metrics

            })

        except Exception as e:

            st.error(
                f"Gemini Error:\n\n{e}"
            )

            st.stop()

    st.divider()

    st.subheader("🤖 AI Career Projection")

    st.success(
        "Projection generated successfully."
    )

    st.markdown(projection)

    st.download_button(
        "📄 Download Projection",
        projection,
        file_name=f"{player['Player']}_AI_Projection.txt",
        mime="text/plain",
        use_container_width=True
    )