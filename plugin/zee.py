import logging
import os
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from imdb import IMDb
from config import API_ID, API_HASH, BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Client(
    "imdb_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Log when the bot starts
logging.info("Bot started. Listening for commands and messages...")

def start_command(update, context):
    update.reply_text("Hello! I'm your IMDb bot. Send me {text} to search on IMDb.")

@Client.on_message(filters.command("start"))
def start(client, message):
    start_command(message, None)

@Client.on_message(filters.text & ~filters.command)
def reply_to_text(client, message):
    content = message.text

    # Extract text between $ and & using regular expressions
    match = re.search(r'\$(.*?)\&', content)
    if match:
        search_text = match.group(1)

        # Search IMDb using 'search_text' and retrieve results
        ia = IMDb()
        search_results = ia.search_movie(search_text)

        if search_results:
            # Get the first three search results
            first_three_results = search_results[:3]
            reply_message = f"IMDb search results for '{search_text}':\n"
            for result in first_three_results:
                title = result['title']
                release_date = result.get('release date', 'N/A')
                release_year = result.get('year', 'N/A')

                if release_date == 'N/A':
                    release_info = f"Release Year: {release_year}"
                else:
                    release_info = f"Release Date: {release_date}"

                reply_message += f"\nTitle: {title}\n{release_info}"

            # Send IMDb search results to the appropriate chat
            client.send_message(chat_id=message.chat.id, text=reply_message)
        else:
            # No search results found, send a message indicating no queries are related
            client.send_message(chat_id=message.chat.id, text=f"No Queries Related {search_text}")

@Client.on_message(filters.command("help"))
def help_command(update, context):
    update.reply_text("Send me a message containing text between $ and & to search on IMDb.")

def keep_bot_alive():
    # Send a "ping" message at regular intervals to keep the bot active
    while True:
        app.send_message(chat_id="@vdhsmdm", text="Bot is active and running!")
        app.loop.run_until_complete(asyncio.sleep(3600))  # Sleep for 1 hour
