import logging
import logging.config
from telegram.ext import Updater, InlineQueryHandler
from utils.imdb_utils import search_imdb

# Load logging configuration from logging.conf file
logging.config.fileConfig('logging.conf')

# Create a logger instance for the bot
logger = logging.getLogger(__name__)

# Set your bot token here
BOT_TOKEN = '1829969794:AAE7BRLnznbiLmWcI8qmw_GoudeGzSzZqHo'

# Define inline query handler
def inline_query(update, context):
    query = update.inline_query.query
    logger.info(f"Received inline query: {query}")

    results = []

    if query:
        imdb_results = search_imdb(query)

        for result in imdb_results:
            title = result['title']
            summary = result['summary']
            imdb_url = result['imdb_url']

            message_content = InputTextMessageContent(f"{title}\n\n{summary}")
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("View on IMDb", url=imdb_url)]])
            results.append({
                'type': 'article',
                'id': str(len(results) + 1),
                'title': title,
                'input_message_content': message_content,
                'reply_markup': reply_markup
            })

    update.inline_query.answer(results)

# Set up the Telegram bot
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Set up inline query handler
    inline_query_handler = InlineQueryHandler(inline_query)
    dispatcher.add_handler(inline_query_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
