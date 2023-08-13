from pyrogram import Client, filters
import re
from imdb import IMDb
from pymongo import MongoClient
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

# Message handler to reply with IMDb information
@Client.on_message(filters.text)
async def reply_to_text(client, message):
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

            # Send the reply
            await client.send_message(message.chat.id, reply_message)
        else:
            # No search results found, provide a suggestion
            suggestion_message = "Spelling mistake! Search correct name on Google then request here."
            await client.send_message(message.chat.id, suggestion_message)
