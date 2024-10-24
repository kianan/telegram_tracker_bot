# Kian Tracker Bot

Kian Tracker Bot is a simple Telegram bot that helps users manage their tasks and log their expenses via the Telegram messaging platform.

## Features
- Responds to the `/start` command with a welcome message.
- Handles user messages and logs expenses.
- Integrates with local Llama model for enhanced data extraction from user messages.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Telegram Bot Token (obtained from BotFather on Telegram)
- `pipenv` for managing the virtual environment
- Ollama (for local Llama model)

### Setup Steps

1. **Clone the repository** and navigate to the project folder:
   ```sh
   git clone <repository-url>
   cd telegram_bot
   ```

2. **Create a virtual environment** using `pipenv` and install the required dependencies:
   ```sh
   pipenv --python 3.9
   pipenv install python-telegram-bot python-dotenv fuzzywuzzy spacy aiohttp dateparser
   ```

3. **Install the SpaCy language model**:
   ```sh
   python -m spacy download en_core_web_lg
   ```

4. **Create a `.env` file** in the root of your project directory and add your Telegram Bot Token:
   ```
   TELEGRAM_BOT_TOKEN=your_actual_bot_token
   AUTHORIZED_USERNAMES=username1,username2
   ```

5. **Install Ollama**:
   - Ollama is required to run the local Llama model. You can install Ollama by following the instructions on their official website: [Ollama Installation](https://ollama.com/docs/installation)

6. **Run Ollama and Download Llama Model**:
   - Start the Ollama service locally:
     ```sh
     ollama serve
     ```
   - Download the Llama model:
     ```sh
     ollama pull llama3.2:1b
     ```

7. **Activate the virtual environment**:
   ```sh
   pipenv shell
   ```

8. **Run the bot**:
   ```sh
   python bot.py
   ```

## Usage
- Start the bot by sending the `/start` command in Telegram.
- You can send any message to log expenses, and the bot will extract relevant details and store them.

## License
This project is open source and available under the MIT License.

