from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from database import get_user, update_user

# 🟢 Menu buttons
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⛏️ Mine", callback_data='mine')],
        [InlineKeyboardButton("⚙️ Upgrade (10 coins)", callback_data='upgrade')],
        [InlineKeyboardButton("📊 Stats", callback_data='stats')],
    ])

# 🟢 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to CoinCrack Bot 💰", reply_markup=get_main_menu())

# 🟢 Button click handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'mine':
        await handle_mine(query, user_id)
    elif query.data == 'upgrade':
        await handle_upgrade(query, user_id)
    elif query.data == 'stats':
        await handle_stats(query, user_id)

# 🟢 Mining logic
async def handle_mine(query, user_id):
    user = await get_user(user_id)
    mined = user['power']
    new_total = user['coins'] + mined
    await update_user(user_id, coins=new_total)
    await query.edit_message_text(f"⛏️ You mined {mined} coins!\nTotal: {new_total} coins", reply_markup=get_main_menu())

# 🟢 Upgrade logic
async def handle_upgrade(query, user_id):
    user = await get_user(user_id)
    if user['coins'] >= 10:
        await update_user(user_id, coins=user['coins'] - 10, power=user['power'] + 1)
        await query.edit_message_text(f"⚙️ Upgrade successful!\nPower: {user['power'] + 1}\nCoins: {user['coins'] - 10}", reply_markup=get_main_menu())
    else:
        await query.edit_message_text("❌ Not enough coins!", reply_markup=get_main_menu())

# 🟢 Stats logic
async def handle_stats(query, user_id):
    user = await get_user(user_id)
    await query.edit_message_text(f"📊 Stats:\nCoins: {user['coins']}\nPower: {user['power']}", reply_markup=get_main_menu())

# 🟢 Optional init_db
async def init_db():
    pass  # You can define DB init logic here if needed
