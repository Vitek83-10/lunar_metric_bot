import asyncio
import logging
import requests
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, LUNAR_API_TOKEN, YOUR_TELEGRAM_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("lunar_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

sent_tokens = set()

async def fetch_lunar_tokens():
    url = f"https://api.lunarcrush.com/v2?data=assets&key={LUNAR_API_TOKEN}&chain=solana"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"LunarCrush API error: {response.status_code}")
            return []

        data = response.json().get("data", [])
        return data
    except Exception as e:
        logger.error(f"Exception while fetching LunarCrush data: {e}")
        return []

def passes_filter(token_data):
    metrics = token_data.get("galaxy_score_metrics", {}).get("twitter", {})
    engagements = metrics.get("tweet_engagement", 0)
    mentions = metrics.get("tweet_mentions", 0)
    creators = metrics.get("tweet_creators", 0)
    sentiment = metrics.get("tweet_sentiment", 0)

    return (
        engagements >= 10 and
        mentions >= 10 and
        creators >= 10 and
        sentiment >= 75
    )

def format_token_message(token_data):
    name = token_data.get("name", "Unknown")
    ca = token_data.get("id", "N/A")
    metrics = token_data.get("galaxy_score_metrics", {}).get("twitter", {})

    mentions = metrics.get("tweet_mentions", 0)
    creators = metrics.get("tweet_creators", 0)
    engagements = metrics.get("tweet_engagement", 0)
    sentiment = metrics.get("tweet_sentiment", 0)

    return f"""🛰 Найден токен:

🔹 **{name}**
• 🗣 Mentions: {mentions}
• 👤 Creators: {creators}
• 💬 Engagements: {engagements}
• ❤️ Sentiment: {sentiment}%

🔗 CA: `{ca}`"""

async def monitor_lunarcrush():
    await app.start()
    while True:
        logger.info("🔍 Сканирую LunarCrush...")
        tokens = await asyncio.to_thread(fetch_lunar_tokens)

        for token in tokens:
            ca = token.get("id")
            if not ca or ca in sent_tokens:
                continue
            if passes_filter(token):
                message = format_token_message(token)
                try:
