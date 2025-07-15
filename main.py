import asyncio
import os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from logic import start, button_handler, init_db

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Make sure to set this in Render environment variables

async def main():
    await init_db()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
