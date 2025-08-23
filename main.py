import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Load FAQ
with open("FAQUTE.json", "r") as f:
    FAQ = json.load(f)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Ask me a question from the FAQ.")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    answer = FAQ.get(user_text, "❌ Sorry, I don’t know the answer to that 🤖")
    await update.message.reply_text(answer)

def main():
    TOKEN = os.getenv("BOT_TOKEN")  # Use env variable for safety
    if not TOKEN:
        print("⚠️ BOT_TOKEN not found. Set it with: $env:BOT_TOKEN='8112802338:AAHc8KKUQ7DjE6Dp0xlOsqjYYJSGdgwf_XE'")
        return
    
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
