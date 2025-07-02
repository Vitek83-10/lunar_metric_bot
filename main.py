import asyncio
from pyrogram import Client, filters
from config import BOT_TOKEN, API_ID, API_HASH
from lunar import fetch_lunar_data, filter_lunar_tokens

bot = Client("lunar_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("👋 Привет! Я готов к работе.\n\nВыберите команду ниже:")

@bot.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply(
        "🛠 Доступные команды:\n"
        "/start — запуск\n"
        "/status — статус\n"
        "/test — тест\n"
        "/help — помощь"
    )

@bot.on_message(filters.command("test"))
async def test_command(client, message):
    await message.reply("🧪 Тестовая команда выполнена успешно!")

@bot.on_message(filters.command("status"))
async def status_command(client, message):
    await message.reply("✅ Бот работает. LunarCrush будет опрашиваться каждые 5 минут.")

async def lunar_polling():
    while True:
        try:
            tokens = await fetch_lunar_data()
            filtered = filter_lunar_tokens(tokens)
            for token in filtered:
                text = (
                    f"🌕 Найден токен:\n"
                    f"• CA: `{token['token']}`\n"
                    f"• Engagements: {token['engagements']}\n"
                    f"• Mentions: {token['mentions']}\n"
                    f"• Creators: {token['creators']}\n"
                    f"• Sentiment: {token['sentiment']}%\n"
                    f"\n💰 Рекомендуется к входу: ДА"
                )
                await bot.send_message(chat_id=message.chat.id, text=text)
        except Exception as e:
            print(f"[ERROR] {e}")
        await asyncio.sleep(300)

async def main():
    await bot.start()
    asyncio.create_task(lunar_polling())
    await idle()

if __name__ == "__main__":
    import nest_asyncio
    from pyrogram import idle
    nest_asyncio.apply()
    asyncio.run(main())
