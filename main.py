import json
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

with open("FAQUTE.json", "r", encoding="utf-8") as f:
    FAQ = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = list(FAQ.keys())
    keyboard = [[c] for c in categories]
    await update.message.reply_text(
        "Welcome! Please choose a category:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

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
    application = Application.builder().token("8112802338:AAHc8KKUQ7DjE6Dp0xlOsqjYYJSGdgwf_XE").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, category_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
