import logging
from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from imdb import IMDb
import os
import re

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Retrieve the Telegram Bot API Token from the environment variable
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your IMDb bot. Send me {text} to search on IMDb.")

def reply_to_text(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.text:
        content = update.message.text

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

                    if release_date != 'N/A':
                        release_info = f"Release Date: {release_date}"
                    else:
                        release_info = f"Release Year: {release_year}"

                    reply_message += f"\nTitle: {title}\n{release_info}"

                # Send IMDb search results to the appropriate chat
                context.bot.send_message(chat_id=update.message.chat_id, text=reply_message)
            else:
                # No search results found, send a message indicating no queries are related
                context.bot.send_message(chat_id=update.message.chat_id, text=f"No Queries Related {search_text}")
        else:
            pass
    else:
        pass

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_text))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
