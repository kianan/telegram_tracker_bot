import requests
import json
import os
import logging
from fuzzywuzzy import process, fuzz
import spacy
import dateparser
from datetime import datetime

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
ollama_api_url = "http://localhost:11434/api/generate"  # Assuming Ollama runs locally on this port

# Load SpaCy model
nlp = spacy.load('en_core_web_lg')

# Function to call local Llama model
def call_local_llama_model(user_message):
    headers = {"Content-Type": "application/json"}
    prompt = f"""Extract the following details as clean JSON: Amount, Date, Category, Account.
    Do not include any other text.
    Send an empty respone if unable to parse.
    Sentence: '{user_message}'"""
    payload = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "temperature": 0.7,
        "stream": False
    }

    try:
        response = requests.post(ollama_api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        logger.info(f"Raw response content: {response.text}")

        response_json = response.json()  # Attempt to parse response as JSON
        logger.info(f"{response_json}")

        return json.loads(response_json.get("response"))
        # return response.json().get("response")
    except requests.RequestException as e:
        logger.error(f"Failed to call local model: {e}")
        return None

# Function to process message using fuzzywuzzy and SpaCy
def process_message_fuzzywuzzy(user_message):
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
            parsed_date = dateparser.parse(ent.text)
            if parsed_date:
                date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

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

    return {
        "amount": amount,
        "date": date,
        "category": category,
        "account": account
    }

# Function to process message using Ollama Llama model
def process_message_ollama(user_message):
    response = call_local_llama_model(user_message)
    if response:
        logger.info(f"Extracted data from Llama - {response}")
        return response
    else:
        logger.error("Failed to extract data using Llama model.")
        return None

# Function to check if Ollama is running
def is_ollama_running():
    try:
        response = requests.get("http://localhost:11434")  # Assuming Ollama has a health check endpoint
        if response.status_code == 200:
            logger.info("Ollama is running.")
            return True
        else:
            logger.warning("Ollama health check returned a non-200 status.")
            return False
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Ollama: {e}")
        return False