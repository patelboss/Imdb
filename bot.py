import logging
from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from imdb import IMDb
import os
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from aiohttp import web
from plugins import web_server

PORT = "8080"

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Retrieve the Telegram Bot API Token from the environment variable
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
        # Search IMDb using 'content' and retrieve results

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        logging.info("Bot Running Now")
        logging.info(LOG_STR)

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")
   
async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat sequentially.
        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_messages` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat messages with a
        single call.
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                
            limit (``int``):
                Identifier of the last message to be returned.
                
            offset (``int``, *optional*):
                Identifier of the first message to be returned.
                Defaults to 0.
        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.
        Example:
            .. code-block:: python
                for message in app.iter_messages("pyrogram", 1, 15000):
                    print(message.text)
        """
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1

                     
def reply_to_content(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.text:
        content = update.message.text
        # Extract content between { and }
        content = content[content.find('{')+1:content.find('}')]

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
  

app = Bot()
app.run()
