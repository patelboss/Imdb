import logging
import logging.config
from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters
from telegram import ParseMode
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

            message_content = title + "\n\n" + summary + f"\nView on [IMDb]({imdb_url})"
            results.append({
                'type': 'article',
                'id': str(len(results) + 1),
                'title': title,
                'input_message_content': message_content,
                'parse_mode': ParseMode.MARKDOWN,
            })

    update.inline_query.answer(results)

# Define group message handler
def group_message(update, context):
    message = update.message.text
    logger.info(f"Received group message: {message}")

    # Check if the message is enclosed within curly braces
    if message.startswith('{') and message.endswith('}'):
        # Extract the text between curly braces
        text_inside_braces = message[1:-1]
        update.message.reply_text(f"Bot received group message: {text_inside_braces}")
    else:
        # Ignore messages that are not enclosed within curly braces
        logger.info("Ignoring group message")

# Set up the Telegram bot
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Set up inline query handler
    inline_query_handler = InlineQueryHandler(inline_query)
    dispatcher.add_handler(inline_query_handler)

    # Set up group message handler
    group_message_handler = MessageHandler(Filters.chat_type.groups & Filters.text, group_message)
    dispatcher.add_handler(group_message_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
