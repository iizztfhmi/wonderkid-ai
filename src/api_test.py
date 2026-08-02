import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALLDATA_API_KEY")

url = "https://footballdata.io/api/v1/search"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

params = {
    "q": "Dean Huijsen",
    "type": "players"
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

print("URL:", response.url)
print("Status:", response.status_code)
print(response.json())