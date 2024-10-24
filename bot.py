import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your bot token from BotFather
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
async def start(update: Update, context):
    await update.message.reply_text('Hi! I am Kian Tracker Bot. How can I help you?')

# Function to handle text messages
async def handle_message(update: Update, context):
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")  # Log the message to the console
    # await update.message.reply_text(f"You said: {user_message}")  # Echo the message back to the user

def main():
    # Print a status message when the script starts
    logger.info("Starting the Telegram bot...")

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