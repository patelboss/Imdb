import logging
from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from imdb import IMDb
import os

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Retrieve the Telegram Bot API Token from the environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

# Safety guidelines
safety_guidelines = ["bad word", "offensive phrase"]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your IMDb bot. Send me {text} to search on IMDb.")
    logging.info("Bot started.")

def reply_to_content(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.text:
        content = update.message.text
        # Extract content between { and }
        content = content[content.find('{')+1:content.find('}')]

        # Search IMDb using 'content' and retrieve results
        ia = IMDb()
        search_results = ia.search_movie(content)
        
        if search_results:
            # Get the first search result (you can modify this to show more results)
            first_result = search_results[0]
            title = first_result['title']
            release_date = first_result.get('release date', 'N/A')
            rating = first_result.get('rating', 'N/A')
            summary = first_result.get('plot outline', 'No summary available')

            # Compose IMDb search results
            reply_message = f"IMDb search results for '{content}':\n"
            reply_message += f"Title: {title}\nRelease Date: {release_date}\nRating: {rating}\nSummary: {summary}"

            # Check if the response violates the safety guidelines
            if not any(word in reply_message for word in safety_guidelines):
                # Send IMDb search results to the appropriate chat
                if update.message.chat.type == Chat.CHANNEL:
                    context.bot.send_message(update.message.chat_id, reply_message)
                else:
                    update.message.reply_text(reply_message)

                logging.info(f"IMDb search results for '{content}': {title}, Release Date: {release_date}, Rating: {rating}, Summary: {summary}")
            else:
                update.message.reply_text(
                    "Sorry, I can't send this message because it violates the safety guidelines."
                )
                logging.warning(
                    f"Not sending IMDb search results for '{content}' because it violates the safety guidelines."
                )
        else:
            update.message.reply_text(f"No IMDb results found for '{content}'.")
            logging.warning(f"No IMDb results found for '{content}'.")
    else:
        logging.warning("Received an empty or non-text message.")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_content))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
