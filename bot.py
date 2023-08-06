from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from imdb import IMDb
from health_check import app as health_check_app
# Define your bot's token
TOKEN = '1829969794:AAE7BRLnznbiLmWcI8qmw_GoudeGzSzZqHo'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your IMDb bot. Send me {text} to search on IMDb.")

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
        year = first_result['year']
        rating = first_result.get('rating', 'N/A')
        summary = first_result.get('plot outline', 'No summary available')

        # Compose IMDb search results
        reply_message = f"IMDb search results for '{content}':\n"
        reply_message += f"Title: {title}\nYear: {year}\nRating: {rating}\nSummary: {summary}"

        # Send IMDb search results to the group
        update.message.reply_text(reply_message)
    else:
        update.message.reply_text("No IMDb results found for '{content}'.")
        logging.warning("Received an empty or non-text message.")
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_content))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
health_check_app.run(host='0.0.0.0', port=8080)  # Run Flask app for health check
