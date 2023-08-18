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
    await message.reply_text("Hello! I'm beta type of @Rashmika_mandanana_bot\n Not Beta I am beta of her. 😂\n I am restricted from public use so try on your own risk 🙏🏻")

# Command handler for /help
@Client.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text("If You have Permission to use me. then do 🙏🏻.")

# Function to perform IMDb search and return results as InlineKeyboardMarkup
def perform_imdb_search(search_text):
    ia = IMDb()
    search_results = ia.search_movie(search_text)

    if search_results:
        keyboard = []
        for i, result in enumerate(search_results[:10], start=1):
            title = result['title']
            year = result.get('year', 'N/A')
            button_text = f"{i}. {title} - {year}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=title)])

        return InlineKeyboardMarkup(keyboard)
    else:
        return None
        
# Message handler for regular text messages
@Client.on_message(filters.text)
async def reply_to_text(client, message):
    search_text = message.text
    inline_keyboard = perform_imdb_search(search_text)

    if inline_keyboard:
        await message.reply_text("Which one do you want? Choose one:", reply_markup=inline_keyboard)
    else:
        # IMDb search not found, provide a suggestion
        suggestion_message = "No results found for '{}'.".format(search_text)
        await message.reply_text(suggestion_message)
        
# Callback handler for inline keyboard buttons
@Client.on_callback_query()
async def callback_query_handler(client, query):
    logging.info("Callback query received.")
    title = query.data.lower()
    logging.info(f"Title: {title}") 

    try:
        mongo_client = MongoClient(DATABASE_URI)
        db = mongo_client['TelegramBot']
        collection = db['TelegramBot']

        # Use a case-insensitive regular expression to find similar titles
        similar_titles = collection.find({"file_name": {"$regex": title, "$options": "i"}})

        if similar_titles.count() > 0:
            reply_message = f"Similar titles found in the database:"
            for movie in similar_titles:
                reply_message += f"\n- {movie['title']}"
        else:
            reply_message = f"No similar titles found in the database."

        await query.message.edit_text(reply_message)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
