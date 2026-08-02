import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv

# ==========================
# Load API Key
# ==========================

load_dotenv()

API_KEY = os.getenv("FOOTBALLDATA_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

SEARCH_URL = "https://footballdata.io/api/v1/search"

# ==========================
# Load FBref Dataset
# ==========================

players = pd.read_csv("data/processed/young_players.csv")

print("=" * 60)
print("WonderKid AI - Player Enrichment")
print("=" * 60)

print(f"Players to search: {len(players)}")

# ==========================
# Store Results
# ==========================

results = []

# ==========================
# Search Every Player
# ==========================

for index, row in players.iterrows():

    player_name = row["Player"]

    print(f"\n[{index+1}/{len(players)}]")
    print("Raw name:", repr(player_name))

    params = {
        "q": player_name,
        "type": "players"
    }

    response = requests.get(
        SEARCH_URL,
        headers=HEADERS,
        params=params
    )

    if response.status_code != 200:
        print("API Error:", response.status_code)
        continue

    data = response.json()

    player_list = data["data"]["results"]["players"]

    if len(player_list) == 0:
        print("Not found.")
        continue

    # First result for now
    player = player_list[0]

    results.append({

        "Player": player_name,

        "API_Name": player["player_name"],

        "Player_ID": player["player_id"],

        "Nationality": player["nationality"],

        "Age_API": player["age"],

        "Height_cm": player["height_cm"],

        "Weight_kg": player["weight_kg"],

        "Broad_Position": player["position_name"]

    })

    print("Found:", player["player_name"])

    # Be nice to the API
    time.sleep(0.3)

# ==========================
# Save Metadata
# ==========================

metadata = pd.DataFrame(results)

os.makedirs("data/enriched", exist_ok=True)

metadata.to_csv(
    "data/enriched/player_metadata.csv",
    index=False
)

print("\nMetadata saved!")
print(metadata.head())