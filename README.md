# Kian Tracker Bot

Kian Tracker Bot is a simple Telegram bot that helps users manage their tasks and log their expenses via the Telegram messaging platform.

## Features
- Responds to the `/start` command with a welcome message.
- Handles user messages and extracts information like amount, date, and category using natural language processing (NLP).
- Logs messages to the console for easy debugging.
- Uses fuzzy matching to categorize expenses, even when spelling errors are present.
- Includes basic error handling for failed connections and invalid bot tokens.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Telegram Bot Token (obtained from BotFather on Telegram)
- `pipenv` for managing the virtual environment

### Setup Steps
1. **Clone the repository** and navigate to the project folder:
   ```sh
   git clone <repository-url>
   cd telegram_bot
   ```

2. **Create a virtual environment** using `pipenv` and install the required dependencies:
   ```sh
   pipenv --python 3.9
   pipenv install python-telegram-bot python-dotenv spacy fuzzywuzzy
   ```

3. **Download the SpaCy language model**:
   ```sh
   pipenv run python -m spacy download en_core_web_lg
   ```

4. **Create a `.env` file** in the root of your project directory and add your Telegram Bot Token:
   ```
   TELEGRAM_BOT_TOKEN=your_actual_bot_token
   ```

5. **Activate the virtual environment**:
   ```sh
   pipenv shell
   ```

6. **Run the bot**:
   ```sh
   python bot.py
   ```

## Logging and Error Handling
- The bot uses the `logging` module to print status messages to the console.
- Basic error handling is included to catch issues such as incorrect bot tokens or connection problems.
- Additional status messages are logged to indicate when the bot starts, is running, or if an error occurs.

## Usage
- Start the bot by sending the `/start` command in Telegram.
- You can also send any message, and the bot will extract and log relevant information like the amount, date, and category.

## License
This project is open source and available under the MIT License.

