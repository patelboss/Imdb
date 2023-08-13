from pyrogram import Client, filters
import re
import os
from imdb import IMDb
from pymongo import MongoClient
from config import API_ID, API_HASH, DATABASE_URI, MY_CHANNEL, BOT_TOKEN
import logging
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log when the bot starts
logging.info("Bot started. Listening for commands and messages...")

def start_command(update, context):
    update.reply_text("Hello! I'm your IMDb bot. Send me {text} to search on IMDb.")

@Client.on_message(filters.command("start"))
def start(client, message):
    start_command(message, None)

@Client.on_message(filters.text)
def reply_to_text(client, message):
    content = message.text

    # Extract text between $ and & using regular expressions
    match = re.search(r'\$(.*?)\&', content)
    if match:
        search_text = match.group(1)
     ia = IMDb()
     mongo_client = MongoClient(DATABASE_URI)
     db = mongo_client['TelegramBot']
     collection = db['TelegramBot']

        # Search IMDb using 'search_text' and retrieve results
        search_results = ia.search_movie(search_text)

        if search_results:
            movie_title = search_results[0]['title']

            # Check if the movie is in the database
            if collection.find_one({'title': movie_title}):
                reply_message = f"The movie '{movie_title}' is already in the database."
            else:
                # Get IMDb details
                imdb_movie = search_results[0]
                title = imdb_movie['title']
                release_date = imdb_movie.get('release date', 'N/A')
                release_year = imdb_movie.get('year', 'N/A')
                rating = imdb_movie.get('rating', 'N/A')

                if release_date == 'N/A':
                    release_info = f"Release Year: {release_year}"
                else:
                    release_info = f"Release Date: {release_date}"

                rating_stars = '⭐' * int(rating) if rating != 'N/A' else 'N/A'
                reply_message = f"Title: {title}\n{release_info}\nRating: {rating_stars}"

            # Send the appropriate reply to the channel
            await client.send_message(message.chat.id, reply_message)
        else:
            # No search results found, provide a suggestion
            suggestion_message = "Spelling mistake! Search correct name on Google then request here."
            await client.send_message(message.chat.id, suggestion_message)
        
@Client.on_message(filters.command("help"))
def help_command(update, context):
    update.reply_text("Send me a message containing text between $ and & to search on IMDb.")
