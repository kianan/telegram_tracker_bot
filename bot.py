import os
import logging
import spacy
import dateparser
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from fuzzywuzzy import process, fuzz
from message_processing import *

# Load environment variables from .env file
load_dotenv()

# Your bot token from BotFather
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# List of authorized usernames
AUTHORIZED_USERNAMES = os.getenv('AUTHORIZED_USERNAMES', '').split(',')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load SpaCy model
nlp = spacy.load('en_core_web_lg')

# Function to handle the /start command
async def start(update: Update, context):
    await update.message.reply_text('Hi! I am Kian Tracker Bot. How can I help you?')

def is_user_authorized(username):
    if username not in AUTHORIZED_USERNAMES:
        logger.warning(f"Unauthorized user: {username}")
        return False
    return True

# Function to handle text messages
async def handle_message(update: Update, context):
    user_message = update.message.text
    logger.info(f"Received message: {update.message.from_user.username} {user_message}")  # Log the message to the console

    username = update.message.from_user.username
    if not is_user_authorized(username):
        logger.warning(f"Unauthorized user: {username}")
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    # Process the message using fuzzywuzzy method
    parsed_data = await process_message_ollama(user_message)
    if parsed_data:
        # change all keys to lowercase
        parsed_data = {k.lower(): v for k, v in parsed_data.items()}

        # Log extracted data
        logger.info(f"Extracted data - Amount: {parsed_data['amount']}, Category: {parsed_data['category']}, Date: {parsed_data['date']}, Account: {parsed_data['account']}")

        # Respond to the user
        response = f"Logged expense - Amount: {parsed_data['amount']}, Category: {parsed_data['category']}, Date: {parsed_data['date']}, Account: {parsed_data['account']}"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Failed to process message. Please try again.")

def main():
    # Print a status message when the script starts
    logger.info("Starting the Telegram bot...")

    # check if ollama is running
    if not is_ollama_running():
        logger.error("Ollama is not running.")
        return

    try:
        # Create the Application and pass it your bot's token
        app = ApplicationBuilder().token(TOKEN).build()

        # Register the /start command
        app.add_handler(CommandHandler("start", start))

        # Register the handler for any text message
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Start the bot
        logger.info("Bot is running...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Failed to start the bot: {e}")

if __name__ == '__main__':
    main()
