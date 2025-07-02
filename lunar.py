import requests
from config import LUNAR_API_TOKEN

LUNAR_API_URL = "https://api.lunarcrush.com/v2"

def fetch_lunar_data():
    params = {
        "data": "market",
        "key": LUNAR_API_TOKEN,
        "limit": 250,
        "market": "solana",
        "sort": "alt_rank",
        "desc": "true"
    }
    response = requests.get(LUNAR_API_URL, params=params)
    response.raise_for_status()
    return response.json()["data"]

def filter_lunar_tokens(data):
    filtered = []
    for token in data:
        engagements = token.get("galaxy_score", 0)
        mentions = token.get("twitter_mentions", 0)
        creators = token.get("twitter_followers", 0)
        sentiment = token.get("average_sentiment", 0)

        if (engagements >= 10 and mentions >= 10 and creators >= 10 and sentiment >= 75):
            filtered.append({
                "name": token.get("name"),
                "symbol": token.get("symbol"),
                "price": token.get("price"),
                "engagements": engagements,
                "mentions": mentions,
                "creators": creators,
                "sentiment": sentiment
            })
    return filtered
