import os
import logging
import spacy
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from fuzzywuzzy import process, fuzz

# Load environment variables from .env file
load_dotenv()

# Your bot token from BotFather
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load SpaCy model
nlp = spacy.load('en_core_web_lg')

# Function to handle the /start command
async def start(update: Update, context):
    await update.message.reply_text('Hi! I am Kian Tracker Bot. How can I help you?')

# Function to handle text messages
async def handle_message(update: Update, context):
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")  # Log the message to the console

    # Use SpaCy to parse the message
    doc = nlp(user_message)

    # Extract entities
    amount = None
    category = None
    date = None
    account = "personal"  # Default to 'personal' if not specified

    for ent in doc.ents:
        if ent.label_ == "MONEY":
            amount = ent.text
        elif ent.label_ == "DATE":
            date = ent.text

    # Enhanced category extraction - use fuzzy matching for tokens
    possible_categories = [
        "lunch", "dinner", "groceries", "food", "entertainment", "transport", "rent", "utilities"
    ]
    highest_similarity = 0.0
    similarity_threshold = 70  # Fuzzy matching threshold (0-100 scale)

    # Use fuzzy matching to find the best category match based on token text
    for token in doc:
        matched_category, match_score = process.extractOne(token.text.lower(), possible_categories, scorer=fuzz.ratio)
        if match_score > highest_similarity and match_score >= similarity_threshold:
            highest_similarity = match_score
            category = matched_category

    # If no category is found, set a default value
    if category is None:
        category = "miscellaneous"

    # If no date is specified, use the current datetime
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log extracted data
    logger.info(f"Extracted data - Amount: {amount}, Category: {category}, Date: {date}, Account: {account}")

    # Respond to the user
    response = f"Logged expense - Amount: {amount}, Category: {category}, Date: {date}, Account: {account}"
    await update.message.reply_text(response)

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
