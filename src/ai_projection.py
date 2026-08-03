import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_projection(player_data):

    prompt = f"""
You are a professional football scout.

Based ONLY on the information below, generate a realistic scouting projection.

Player:
{player_data["player"]}

Current Club:
{player_data["club"]}

Age:
{player_data["age"]}

Nationality:
{player_data["nationality"]}

Primary Position:
{player_data["position"]}

WonderKid Score:
{player_data["score"]:.2f}/100

Position Ranking:
{player_data["rank"]} of {player_data["total"]}

Statistics:
{player_data["metrics"]}

Instructions:
- Keep every section SHORT (maximum 2 sentences).
- Do NOT invent statistics.
- Base your reasoning on the supplied statistics.
- If the player already plays for an elite club, recommend staying there unless another move is clearly justified.
- If the player has already made his senior international debut, state that instead of predicting a call-up.
- Do not assume whether a player has already debuted for the senior national team.
- If there is insufficient information provided, write a general international outlook based on the player's ability and development instead of stating they will receive a call-up.
- Output ONLY the following sections.


Return exactly this format:

Profile Summary

Best Next Club
Reason:

Best League
Reason:

National Team Outlook

"""

    response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

    return response.text

if __name__ == "__main__":

    projection = generate_projection({
        "player": "Arda Güler",
        "club": "Real Madrid",
        "age": 20,
        "nationality": "Turkey",
        "position": "CAM",
        "score": 90.95,
        "rank": 2,
        "total": 16,
        "metrics": {
            "Goals": 3,
            "Assists": 3,
            "xG": 2.3,
            "xA": 2.0,
            "Key Passes": 22,
            "Progressive Passes": 47,
            "Progressive Carries": 12,
            "Tackles": 13,
            "Interceptions": 2,
            "Clearances": 3
        }
    })

    print(projection)