import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from database import init_db, get_user
from bot_logic import handle_mine, handle_upgrade, handle_stats, get_main_menu

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await get_user(user_id)
    await update.message.reply_text("Welcome to CoinCrackBot ⛏️", reply_markup=get_main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data == "mine":
        await handle_mine(query, user_id)
    elif data == "upgrade":
        await handle_upgrade(query, user_id)
    elif data == "stats":
        await handle_stats(query, user_id)

# ✅ Correct run_polling method for python-telegram-bot v20+
async def main():
    await init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
