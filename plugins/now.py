from pyrogram import Client, filters
import re
from imdb import IMDb
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, DATABASE_URI, BOT_TOKEN
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info("Bot started. Listening for commands and messages...")

# Command handler for /start
@Client.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! I'm your IMDb bot. Send me {text} to search on IMDb.")

# Command handler for /help
@Client.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text("Send me a message containing text between $ and & to search on IMDb.")
from pyrogram import Client, filters
from imdb import IMDb
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, DATABASE_URI, BOT_TOKEN
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info("Bot started. Listening for commands and messages...")

# Initialize the Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to perform IMDb search and return top 3 results as a string
def perform_imdb_search(search_text):
    ia = IMDb()
    search_results = ia.search_movie(search_text)

    if search_results:
        keyboard = []
        for i, result in enumerate(search_results[:3], start=1):
            title = result['title']
            release_date = result.get('release date', result.get('year', 'N/A'))
            keyboard.append([InlineKeyboardButton(f"{i}. {title} - {release_date}", callback_data=title)])

        return InlineKeyboardMarkup(keyboard)
    else:
        return None

# Message handler for text messages
@app.on_message(filters.text & filters.incoming)
async def reply_to_text(client, message):
    content = message.text
    chat_id = message.chat.id

    # Extract the whole text as search_text
    search_text = content

    if message.chat.type == 'channel' and '$' in content and '&' in content:
        match = re.search(r'\$(.*?)\&', content)
        if match:
            search_text = match.group(1)
            inline_keyboard = perform_imdb_search(search_text)
            if inline_keyboard:
                await app.send_message(chat_id, "Top IMDb results:", reply_markup=inline_keyboard)
            else:
                # IMDb search not found, provide a suggestion
                suggestion_message = "Spelling Galat Hai!"
                await app.send_message(chat_id, suggestion_message)
        return
    
    inline_keyboard = perform_imdb_search(search_text)

    if inline_keyboard:
        if message.chat.type == 'channel':
            await app.send_message(chat_id, "Top IMDb results:", reply_markup=inline_keyboard)
        else:
            await message.reply_text("Select a movie:", reply_markup=inline_keyboard)
    else:
        # IMDb search not found, provide a suggestion
        suggestion_message = "Spelling Galat Hai!"
        if message.chat.type == 'channel':
            await app.send_message(chat_id, suggestion_message)
        else:
            await message.reply_text(suggestion_message)

# Callback handler for inline keyboard buttons
@app.on_callback_query()
async def callback_query_handler(client, query):
    title = query.data
    ia = IMDb()
    mongo_client = MongoClient(DATABASE_URI)
    db = mongo_client['TelegramBot']
    collection = db['TelegramBot']

    # Check if the movie is in the database
    if collection.find_one({'title': title}):
        reply_message = f"The movie '{title}' is already in the database."
    else:
        # Add movie title to the database
        collection.insert_one({'title': title})
        reply_message = f" Please Add '{title}' to the database."

    await query.message.edit_text(reply_message)
