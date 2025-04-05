import logging
import gspread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from oauth2client.service_account import ServiceAccountCredentials
from re import fullmatch

# Logging for debugging
logging.basicConfig(level=logging.INFO)

# --- Google Sheets Setup ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
import json
import os

with open("credentials.json", "r") as f:
    creds_dict = json.load(f)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("telegram bot").sheet1

# --- Telegram Bot Token ---
TOKEN = "8065448213:AAHGTJpPBPHm_OOShGzlPrkgujM8XJqt2M8"

# --- Message Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Only process if it's a 10-digit number
    if not fullmatch(r"\d{10}", text):
        return

    # Get all records
    records = sheet.get_all_values()
    headers = records[0]
    data_rows = records[1:]

    for row in data_rows:
        if row[3] == text:
            reply_text = (
                "📂 *Match Found✅*\n"
                f"📅 *Date:* {row[0]}\n"
                f"🧾 *FIR Number:* {row[1]}\n"
                f"👤 *Name:* {row[2]}\n"
                f"📱 *Phone:* {row[3]}\n"
                f"🎂 *Age:* {row[4]}\n"
                f"📌 *Address:* {row[5]}\n"
                "\n *Powered by Alpha🐺*"
            )
            await update.message.reply_text(
                reply_text,
                parse_mode="Markdown",
                reply_to_message_id=update.message.message_id
            )
            return

    # If no match found
    await update.message.reply_text(
        "⚠️ No Match found for this number.",
        reply_to_message_id=update.message.message_id
    )

# --- Run Bot ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^\d{10}$"), handle_message))

print("🤖 Bot is running...")
app.run_polling()
