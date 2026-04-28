import sqlite3
import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= TOKEN (SECURE) =================
# 👉 Option 1: Environment variable (recommended)
TOKEN = "8631688955:AAEJkTGwQfN3Aq-tSSaIgLyP1MUgVt2QlUA"

# 👉 Option 2 (easy test): put token directly
# TOKEN = "PASTE_YOUR_NEW_TOKEN_HERE"

ADMIN_ID = 123456789  # change to your Telegram ID

# ================= IMAGE =================
IMG = "https://i.ibb.co/HTdvDjFj/gamepostert.jpg"

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")
conn.commit()

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?)", (user_id,))
    conn.commit()

def get_users():
    cursor.execute("SELECT user_id FROM users")
    return cursor.fetchall()

# ================= MENU =================
def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["👉 ចុចបើកអាខោនហ្គេម"],
            ["📞 ទាក់ទងក្រុមការងារ"],
            ["🚀 ការផ្តល់ជូនពិសេស"]
        ],
        resize_keyboard=True
    )

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.message.from_user.id)

    await update.message.reply_text(
        "👋 សូមស្វាគមន៍បងមកកាន់ក្រុមហ៊ុនខាងអូ​ន!\n👉 ចុចទីនេះដើម្បីបើកអាខោនណាបងៗ: https://t.me/ET_168_page",
        reply_markup=main_menu()
    )

# ================= HANDLER =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "👉 ចុចបើកអាខោនហ្គេម":
        keyboard = [
            [InlineKeyboardButton("🎮 ចុចទីនេះ", url="https://t.me/ET_168_page")]
        ]

        await update.message.reply_photo(
            photo=IMG,
            caption="👉 ចុចលីងខាងក្រោមដើម្បីចូលលេង",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif text == "📞 ទាក់ទងក្រុមការងារ":
        await update.message.reply_photo(
            photo=IMG,
            caption="📞 ក្រុមការងារបម្រើ 24/7\n👉 https://t.me/ET_168_page"
        )

    elif text == "🚀 ការផ្តល់ជូនពិសេស":
        keyboard = [
            [InlineKeyboardButton("🎁 ចុចទទួលកាដូរ", url="https://t.me/ET_168_page")]
        ]

        await update.message.reply_photo(
            photo=IMG,
            caption="🎁 ទទួលបានកាដូរ ១០០% សម្រាប់អតិថិជនថ្មី!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:
        await update.message.reply_text(
            "👉 សូមជ្រើសពី Menu",
            reply_markup=main_menu()
        )

# ================= BROADCAST =================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast message")
        return

    msg = " ".join(context.args)
    users = get_users()

    sent = 0
    for u in users:
        try:
            await context.bot.send_message(chat_id=u[0], text=msg)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"✅ Sent: {sent}")

# ================= ERROR =================
async def error_handler(update, context):
    print("ERROR:", context.error)

# ================= RUN BOT =================
if TOKEN is None:
    print("❌ ERROR: BOT_TOKEN is not set!")
    exit()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.add_error_handler(error_handler)

print("🔥 Bot is running...")
app.run_polling()