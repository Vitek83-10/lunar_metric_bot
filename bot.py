from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup

import os
import logging

# ✅ Включаем логирование
logging.basicConfig(level=logging.INFO)

# ✅ Конфигурация бота
API_ID = 20234202
API_HASH = "fc0e099e810cbea903512acef8563b36"
BOT_TOKEN = "7587000383:AAFZKVttoUHcACMXrw2I2rWC4kQ47ExPtdg"

# ✅ Создаём клиент
app = Client("lunar_metric_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Меню команд
menu = ReplyKeyboardMarkup(
    [
        ["/start", "/status"],
        ["/help", "/test"]
    ],
    resize_keyboard=True
)

# ✅ Команда /start
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("👋 Привет! Я готов к работе.\nВыберите команду ниже:", reply_markup=menu)

# ✅ Команда /status
@app.on_message(filters.command("status"))
async def status(client, message: Message):
    await message.reply("✅ Бот активен и работает.")

# ✅ Команда /help
@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await message.reply("🛠 Доступные команды:\n/start — запуск\n/status — статус\n/test — тест\n/help — помощь")

# ✅ Команда /test
@app.on_message(filters.command("test"))
async def test_command(client, message: Message):
    await message.reply("🧪 Тестовая команда выполнена успешно!")

# ✅ Запуск
if __name__ == "__main__":
    app.run()
