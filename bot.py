from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup

# 🔐 Токен от Виктора
BOT_TOKEN = "7587000383:AAFZKVttoUHcACMXrw2I2rWC4kQ47ExPtdg"
API_ID = 20234202
API_HASH = "fc0e099e810cbea903512acef8563b36"

# ⚙️ Инициализация клиента
app = Client("LunarMetricBot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# 📌 Клавиатура «Меню»
menu_keyboard = ReplyKeyboardMarkup(
    [["/start", "/help"], ["/check"]],
    resize_keyboard=True,
    one_time_keyboard=False
)

# 🟢 Команда /start
@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text(
        "👋 Бот активен и готов к работе.\n\n"
        "✅ Используй /check <адрес токена>, чтобы получить метрики LunarCrush.",
        reply_markup=menu_keyboard
    )

# 📘 Команда /help
@app.on_message(filters.command("help"))
async def help_handler(client, message: Message):
    await message.reply_text(
        "ℹ️ Команды бота:\n"
        "/start — Перезапустить бота\n"
        "/help — Показать это сообщение\n"
        "/check <CA> — Проверка токена по адресу (Solana)"
    )

# 🔍 Команда /check
@app.on_message(filters.command("check"))
async def check_handler(client, message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("❗ Пример команды: /check CA_ADDRESS")
        return

    ca_address = args[1]
    # 👇 Заглушка: здесь можно подключить реальный API LunarCrush
    await message.reply_text(f"🔎 Проверяю токен: `{ca_address}`\n(Метрики LunarCrush скоро будут здесь)", parse_mode="Markdown")


# 🚀 Запуск
app.run()
