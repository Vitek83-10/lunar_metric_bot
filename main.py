import asyncio
import logging
import os
import requests
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH, LUNAR_API_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client("lunar_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

FILTER_ENGAGEMENTS = 10
FILTER_MENTIONS = 10
FILTER_CREATORS = 10
FILTER_SENTIMENT = 75

# Получение всех токенов с LunarCrush
async def get_lunar_tokens():
    url = f"https://api.lunarcrush.com/v2?data=market&key={LUNAR_API_TOKEN}&chain=solana"
    resp = requests.get(url)
    if resp.status_code != 200:
        return []
    data = resp.json().get("data", [])
    return data

# Отправка метрик
async def monitor_lunarcrush():
    await app.start()
    me = await app.get_me()
    logger.info(f"Бот @{me.username} начал мониторинг LunarCrush")

    while True:
        try:
            tokens = await get_lunar_tokens()
            for token in tokens:
                try:
                    metrics = token.get("galaxy_score_metrics", {}).get("twitter", {})
                    engagements = metrics.get("tweet_engagement", 0)
                    mentions = metrics.get("tweet_mentions", 0)
                    creators = metrics.get("tweet_creators", 0)
                    sentiment = metrics.get("tweet_sentiment", 0)

                    if (
                        engagements >= FILTER_ENGAGEMENTS and
                        mentions >= FILTER_MENTIONS and
                        creators >= FILTER_CREATORS and
                        sentiment >= FILTER_SENTIMENT
                    ):
                        name = token.get("name", "Unknown")
                        ca = token.get("id", "CA Not Found")

                        text = f"""📡 Найден токен:

• 🪙 Имя: {name}
• 🗣 Mentions: {mentions}
• 👤 Creators: {creators}
• 💬 Engagements: {engagements}
• ❤️ Sentiment: {sentiment}%

✅ Проходит фильтр

🔗 CA: `{ca}`"""

                        await app.send_message(chat_id="me", text=text)
                        await asyncio.sleep(1)

                except Exception as inner_err:
                    logger.warning(f"Ошибка в токене: {inner_err}")

        except Exception as e:
            logger.error(f"Ошибка мониторинга: {e}")

        await asyncio.sleep(60)  # проверка раз в минуту

if __name__ == "__main__":
    asyncio.run(monitor_lunarcrush())
