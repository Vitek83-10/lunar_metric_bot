from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    name="LunarMetricBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode="HTML"
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 Привет! Я готов к работе.\nВыберите команду ниже:",
        reply_markup={
            "keyboard": [[
                {"text": "/start"}, {"text": "/status"}
            ], [
                {"text": "/help"}, {"text": "/test"}
            ]],
            "resize_keyboard": True
        }
    )

@bot.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply(
        "🛠 <b>Доступные команды:</b>\n"
        "/start — запуск\n"
        "/status — статус\n"
        "/test — тест\n"
        "/help — помощь"
    )

@bot.on_message(filters.command("status"))
async def status(client, message):
    await message.reply("📡 Бот работает в штатном режиме.")

@bot.on_message(filters.command("test"))
async def test(client, message):
    await message.reply("🧪 Тестовая команда выполнена успешно!")

bot.run()
