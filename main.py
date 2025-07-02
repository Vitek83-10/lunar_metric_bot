from pyrogram import Client, filters
from lunar import fetch_lunar_data, filter_lunar_tokens
from config import BOT_TOKEN, API_ID, API_HASH

app = Client("lunar_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("👋 Бот запущен и готов к фильтрации LunarCrush токенов!")

@app.on_message(filters.command("check"))
async def check_lunar(client, message):
    try:
        data = fetch_lunar_data()
        filtered = filter_lunar_tokens(data)

        if not filtered:
            await message.reply("❌ Нет подходящих токенов по метрикам LunarCrush.")
            return

        for token in filtered[:10]:  # максимум 10 токенов в ответ
            msg = (
                f"📈 <b>{token['name']} ({token['symbol']})</b>\n"
                f"💰 Цена: ${token['price']:.6f}\n"
                f"🔥 Engagements: {token['engagements']}\n"
                f"💬 Mentions: {token['mentions']}\n"
                f"🧑‍💻 Creators: {token['creators']}\n"
                f"📊 Sentiment: {token['sentiment']}%"
            )
            await message.reply(msg, parse_mode="HTML")

    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {e}")

app.run()
