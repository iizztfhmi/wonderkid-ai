import streamlit as st
import pandas as pd
from pathlib import Path


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="WonderKid AI",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Load Custom CSS
# ==========================================================
from pathlib import Path

# Get the folder where app.py is located
BASE_DIR = Path(__file__).parent

# styles.css is in the same folder as app.py
css_file = BASE_DIR / "style.css"

if css_file.exists():
    st.markdown(
        f"<style>{css_file.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )
else:
    st.error(f"style.css not found: {css_file}")


# ==========================================================
# Load Rankings
# ==========================================================

@st.cache_data
def load_rankings():

    ranking_path = Path("data/rankings")

    rankings = {}

    if ranking_path.exists():

        for file in ranking_path.glob("*_rankings.csv"):

            position = file.stem.replace("_rankings", "")

            rankings[position] = pd.read_csv(file)

    return rankings


rankings = load_rankings()


# ==========================================================
# HOME PAGE
# ==========================================================


st.title("WonderKid AI")

st.subheader(
        "AI Football Scouting Platform"
    )

st.markdown("---")

st.write(
        """
WonderKid AI is an AI-powered football scouting platform designed
to evaluate elite Under-21 football talents through statistical
analysis, position-based scoring and artificial intelligence.

The system automatically evaluates every player according
to their natural position and generates professional scouting
reports together with AI future projections.
"""
    )

st.markdown("")

    # --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:

        st.metric(

            label="Players",

            value="81"

        )

with c2:

        st.metric(

            label="Positions",

            value="9"

        )

with c3:

        st.metric(

            label="Statistics",

            value="274"

        )

with c4:

        st.metric(

            label="AI Model",

            value="Gemini"

        )

st.markdown("---")

left, right = st.columns(2)

    # ==================================================

with left:

        st.subheader("Core Features")

        st.markdown("""

✓ Position-Based Scoring

✓ WonderKid Score

✓ Statistical Analysis

✓ Position Rankings

✓ AI Scouting Reports

✓ AI Future Projection

✓ Recommendation Engine

✓ Elite WonderKid Classification

""")

    # ==================================================

with right:

        st.subheader("Supported Positions")

        st.markdown("""

• ST

• LW

• RW

• CAM

• CM

• CDM

• LB

• RB

• CB

""")

st.markdown("---")

st.subheader("Project Workflow")

st.markdown("""

1. Import FBref player statistics

2. Merge all datasets

3. Split players into their natural positions

4. Calculate position-specific WonderKid Scores

5. Rank players within every position

6. Generate scouting reports

7. Generate AI future projections using Gemini

8. Display results through an interactive dashboard

""")

st.markdown("---")

st.subheader("System Overview")

c1, c2, c3 = st.columns(3)

with c1:

        st.info(
            """
Dataset

81 WonderKids

274 Statistics

FBref Performance Data
"""
        )
with c2:

        st.success(
            """
Scouting Engine

Position Models

Weighted Metrics

WonderKid Score
"""
        )

with c3:

        st.warning(
            """
Artificial Intelligence

Gemini

Future Projection

Career Recommendation
"""
        )

st.markdown("---")

st.caption(
        "Use the navigation menu on the left to explore WonderKid AI."
    )

# ==========================================================
# WONDERKID LIST
# ==========================================================



st.title("WonderKid List")

st.write(
        "This page will display all wonderkids with search, filtering and sorting."
    )

# ==========================================================
# PLAYER REPORT
# ==========================================================


st.title("Player Report")

st.write(
        "This page will connect directly to scouting_report.py."
    )

# ==========================================================
# POSITION RANKINGS
# ==========================================================

st.title("Position Rankings")

st.write(
        "Position rankings will be displayed here."
    )

# ==========================================================
# AI PROJECTION
# ==========================================================


st.title("AI Future Projection")

st.write(
        "Gemini AI Future Projection will be displayed here."
    )

# ==========================================================
# ABOUT
# ==========================================================


st.title("About WonderKid AI")

st.subheader("AI Football Scouting Platform")

st.markdown("---")

st.write("""

WonderKid AI is a football scouting platform developed
to evaluate elite Under-21 football talents using
advanced football statistics and Artificial Intelligence.

Technology Stack

• Python

• Pandas

• Streamlit

• Google Gemini AI

• FBref Dataset

• Position-Based Scoring Models

""")

st.markdown("---")

st.caption("WonderKid AI © 2026")