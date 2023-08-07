import logging
import os
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from imdb import IMDb

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize Pyrogram client
API_ID = 4063950
API_HASH = 5ebe4b5c0a2af776bf5d2e52d7f5aaa4
BOT_TOKEN = 1829969794:AAE7BRLnznbiLmWcI8qmw_GoudeGzSzZqHo


app = Client(
    "imdb_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def start_command(update, context):
    update.reply_text("Hello! I'm your IMDb bot. Send me {text} to search on IMDb.")

@app.on_message(filters.command("start"))
def start(client, message):
    start_command(message, None)

@app.on_message(filters.text & ~filters.command)
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

                reply_message += f"\nTitle: {title}\nRelease Date: {release_date}"

            # Send IMDb search results to the appropriate chat
            client.send_message(chat_id=message.chat.id, text=reply_message)
        else:
            # No search results found, send a message indicating no queries are related
            client.send_message(chat_id=message.chat.id, text=f"No Queries Related {search_text}")

@app.on_message(filters.command("help"))
def help_command(update, context):
    update.reply_text("Send me a message containing text between $ and & to search on IMDb.")

if __name__ == "__main__":
    app.run()
