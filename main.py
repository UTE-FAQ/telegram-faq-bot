import os
import json
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Load FAQ JSON
with open("FAQUTE.json", "r", encoding="utf-8") as f:
    FAQ = json.load(f)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = list(FAQ.keys())
    keyboard = [[c] for c in categories]
    await update.message.reply_text(
        "Welcome! Please choose a category:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

# Handle categories and questions
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text
    if category in FAQ:
        questions = list(FAQ[category].keys())
        keyboard = [[q] for q in questions] + [["Back to Categories"]]
        await update.message.reply_text(
            f"Choose a question from {category}:",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
    else:
        for cat, qa in FAQ.items():
            if update.message.text in qa:
                await update.message.reply_text(qa[update.message.text])
                return
        if update.message.text == "Back to Categories":
            await start(update, context)
        else:
            await update.message.reply_text("Sorry, I don’t understand. Please choose from the menu.")

def main():
    # Secure token from environment variable
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN not set. Please configure your environment.")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, category_handler))

    # Run bot
    application.run_polling()

if __name__ == "__main__":
    main()
