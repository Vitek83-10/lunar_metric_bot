async def check_lunar_metrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❗ Пример команды: /check CA_ADDRESS")
        return

    ca = context.args[0]

    url = f"https://lunarcrush.com/api/v3/memo/token/sol/{ca}"
    headers = {
        "Authorization": f"Bearer {LUNAR_API_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        metrics = data.get("data", {}).get("metrics", {})

        engagements = metrics.get("twitter", {}).get("engagements", 0)
        mentions = metrics.get("twitter", {}).get("mentions", 0)
        creators = metrics.get("twitter", {}).get("original_posts", 0)
        sentiment = metrics.get("twitter", {}).get("sentiment", 0)

        passed = (
            engagements >= 10 and
            mentions >= 10 and
            creators >= 10 and
            sentiment >= 75
        )

        if passed:
            result = (
                f"✅ *Метрики пройдены:*\n"
                f"• Engagements: {engagements}\n"
                f"• Mentions: {mentions}\n"
                f"• Creators: {creators}\n"
                f"• Sentiment: {sentiment}%\n\n"
                f"`{ca}`"
            )
        else:
            result = (
                f"❌ *Недостаточно метрик:*\n"
                f"• Engagements: {engagements}\n"
                f"• Mentions: {mentions}\n"
                f"• Creators: {creators}\n"
                f"• Sentiment: {sentiment}%\n\n"
                f"`{ca}`"
            )

        await update.message.reply_markdown(result)

    except Exception as e:
        await update.message.reply_text(f"Ошибка запроса: {e}")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Бот активен. Используй /check <адрес токена>")

# Запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_lunar_metrics))

    print("✅ LunarMetricBot запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
