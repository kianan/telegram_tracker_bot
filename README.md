# Kian Tracker Bot

Kian Tracker Bot is a simple Telegram bot that helps users manage their tasks and log their expenses via the Telegram messaging platform.

## Features
- Responds to the `/start` command with a welcome message.
- Handles user messages and echoes them back for testing purposes.
- Logs messages to the console for easy debugging.

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
   pipenv install python-telegram-bot python-dotenv
   ```

3. **Create a `.env` file** in the root of your project directory and add your Telegram Bot Token:
   ```
   TELEGRAM_BOT_TOKEN=your_actual_bot_token
   ```

4. **Activate the virtual environment**:
   ```sh
   pipenv shell
   ```

5. **Run the bot**:
   ```sh
   python bot.py
   ```

## Usage
- Start the bot by sending the `/start` command in Telegram.
- You can also send any message, and the bot will echo it back to you while logging it in the console.

## License
This project is open source and available under the MIT License.