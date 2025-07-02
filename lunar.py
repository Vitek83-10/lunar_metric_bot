import requests
from config import LUNAR_API_KEY

def fetch_lunar_data():
    url = "https://lunarcrush.com/api3/projects/trending"
    headers = {"Authorization": f"Bearer {LUNAR_API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

def filter_lunar_tokens(data):
    filtered = []
    for token in data.get("data", []):
        if (token.get("social_score", 0) >= 10 and
            token.get("social_mentions", 0) >= 10 and
            token.get("social_contributors", 0) >= 10 and
            token.get("average_sentiment", 0) >= 75):
            filtered.append(token)
    return filtered
