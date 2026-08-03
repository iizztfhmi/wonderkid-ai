import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from pathlib import Path

st.title("WonderKid List")



# ==========================================================
# Load Custom CSS
# ==========================================================





def load_players():

    folder = Path("data/rankings")

    tables = []

    for file in folder.glob("*_rankings.csv"):

        position = file.stem.replace("_rankings", "")

        df = pd.read_csv(file)

        score_col = position + "_Score"

        df["Best Position"] = position
        df["WonderKid Score"] = df[score_col]

        tables.append(df)

    return pd.concat(tables, ignore_index=True)


players = load_players()

players = (
    players
    .sort_values("WonderKid Score", ascending=False)
    .drop_duplicates(subset="Player", keep="first")
    .reset_index(drop=True)
)



positions = ["All"] + sorted(players["Best Position"].unique())

selected_position = st.selectbox(
    "Filter by Position",
    positions
)

search = st.text_input("Search Player")

filtered = players.copy()

if selected_position != "All":
    filtered = filtered[
        filtered["Best Position"] == selected_position
    ]

if search:
    filtered = filtered[
        filtered["Player"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

filtered = filtered.sort_values(
    "WonderKid Score",
    ascending=False
)

display = filtered[
    [
        "Player",
        "Age_y",
        "Squad",
        "PrimaryPosition",
        "SecondaryPosition",
        "ThirdPosition",
        "Height_cm",
        "Nationality",
        "WonderKid Score",
    ]
].rename(columns={
    "Age_y": "Age",
    "Squad": "Club",
    "PrimaryPosition": "Primary",
    "SecondaryPosition": "Secondary",
    "ThirdPosition": "Third",
    "Height_cm": "Height (cm)"
})



display["WonderKid Score"] = (
    display["WonderKid Score"]
    .round()
    .astype(int)
)

# ==========================================================
# Build AgGrid
# ==========================================================

gb = GridOptionsBuilder.from_dataframe(display)

# Default settings
gb.configure_default_column(
    flex=1,
    minWidth=100,
    resizable=True,
    sortable=True,
    filter=True,
)

# Individual columns
gb.configure_column("Player", flex=2)
gb.configure_column("Age", maxWidth=80)
gb.configure_column("Club", flex=2)
gb.configure_column("Primary", flex=1)
gb.configure_column("Secondary", flex=1)
gb.configure_column("Third", flex=1)
gb.configure_column("Height (cm)", maxWidth=120)
gb.configure_column("Nationality", flex=2)
gb.configure_column("WonderKid Score", maxWidth=170)

# Pagination
gb.configure_pagination(
    enabled=True,
    paginationPageSize=15,
)

# Selection
gb.configure_selection(
    selection_mode="single",
    use_checkbox=False,
)

# Grid options
gb.configure_grid_options(
    headerHeight=60,
)

grid_options = gb.build()

# ==========================================================
# Custom CSS
# ==========================================================

custom_css = {
    ".ag-root-wrapper": {
        "background-color": "#0D1420",
        "border": "1px solid #00D9FF",
        "border-radius": "10px",
    },
    ".ag-header": {
        "background-color": "#0A0F1A",
    },
    ".ag-header-cell-label": {
        "color": "#00D9FF",
        "font-size": "13px",
        "font-weight": "700",
        "white-space": "normal",
        "line-height": "18px",
    },
    ".ag-cell": {
        "background-color": "#101B2B",
        "color": "#E7ECF5",
    },
}

# ==========================================================
# Display Grid
# ==========================================================

response = AgGrid(
    display,
    gridOptions=grid_options,
    custom_css=custom_css,
    height=700,
    theme="streamlit",
    fit_columns_on_grid_load=True,
)
