import logging
from pyrogram import Client, filters
import requests
import os
import asyncio

# Логи
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Переменные
BOT_TOKEN = "7587000383:AAFZKVttoUHcACMXrw2I2rWC4kQ47ExPtdg"
API_ID = 20234202
API_HASH = "fc0e099e810cbea903512acef8563b36"
LUNAR_API_TOKEN = "dcovsxshktuhbwvqtuxgx5v3l7gc1ffzq2xr96s5lz0i8v51"  # ✅ Полный

app = Client("lunar_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Обработчик команды /start
@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply("👋 Бот активен. Отправь CA токена, и я покажу метрики из LunarCrush.")

# Обработка сообщения с адресом токена
@app.on_message(filters.text & ~filters.command(["start"]))
async def token_handler(client, message):
    token_address = message.text.strip()

    if not token_address.startswith("0x") and len(token_address) < 32:
        await message.reply("⚠️ Пожалуйста, отправь валидный адрес токена (начинается с 0x или длина от 32 символов).")
        return

    await message.reply("⏳ Запрашиваю данные из LunarCrush...")
    try:
        data = get_lunar_metrics(token_address)
        if not data:
            await message.reply("❌ Не удалось найти метрики LunarCrush для этого токена.")
            return

        response = format_lunar_response(data, token_address)
        await message.reply(response, disable_web_page_preview=True)

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.reply("❌ Произошла ошибка при запросе к LunarCrush.")

# Функция запроса к LunarCrush
def get_lunar_metrics(ca_address):
    url = f"https://api.lunarcrush.com/v2?data=assets&key={LUNAR_API_TOKEN}&symbol={ca_address}&chain=solana"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if "data" not in data or len(data["data"]) == 0:
        return None
    return data["data"][0]

# Форматирование ответа
def format_lunar_response(data, ca):
    engagements = data.get("galaxy_score_metrics", {}).get("twitter", {}).get("tweet_engagement", 0)
    mentions = data.get("galaxy_score_metrics", {}).get("twitter", {}).get("tweet_mentions", 0)
    creators = data.get("galaxy_score_metrics", {}).get("twitter", {}).get("tweet_creators", 0)
    sentiment = data.get("galaxy_score_metrics", {}).get("twitter", {}).get("tweet_sentiment", 0)

    verdict = "✅ Проходит фильтр" if (
        engagements >= 10 and mentions >= 10 and creators >= 10 and sentiment >= 75
    ) else "❌ Не проходит фильтр"

    return f"""📊 Метрики LunarCrush:

• 🗣 Mentions: {mentions}
• 👤 Creators: {creators}
• 💬 Engagements: {engagements}
• ❤️ Sentiment: {sentiment}%

{verdict}

🔗 Token CA: `{ca}`"""

# Запуск
if __name__ == "__main__":
    print("🚀 LunarMetric_Bot запущен.")
    app.run()
