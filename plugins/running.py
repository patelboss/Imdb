import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from config import *
from plugins.translation import Translation
from user import User
from pyrogram import errors
import logging
from bot import Bot
from telegram.client import Telegram

FROM = FROM_CHANNEL
TO = TO_CHANNEL
FILTER = FILTER_TYPE

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@Client.on_message(filters.private & filters.command(["run"]))
async def run(bot, message):
    logging.info("Received /run command")
    if str(message.from_user.id) not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return
    
    buttons = [[
        InlineKeyboardButton('🚫 𝐒𝐓𝐎𝐏', callback_data='stop_btn')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    m = await bot.send_message(
        text="<i>File Forwording Started😉 Join @World_MovieZz</i>",
        reply_markup=reply_markup,
        chat_id=message.chat.id
    )

    files_count = 0
    async for message in bot.USER.search_messages(chat_id=FROM, offset=SKIP_NO, limit=LIMIT, filter=FILTER):
        logging.info("Searching Message")
        try:
            if message.video:
                file_name = message.video.file_name
            else:
                file_name = None
            await bot.copy_Message(from_chat_id=FROM, chat_id=TO, message_id=message.message_id)
            logging.info("copy message")
            files_count += 1
            await asyncio.sleep(1)
            logging.info("sleep 💤")
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            print(e)
            pass
   # await m.delete()
    buttons = [[
        InlineKeyboardButton('📜 𝐔𝐩𝐝𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/world_MovieZz')
    ]] 
    reply_markup = InlineKeyboardMarkup(buttons)
    await m.edit(
        text=f"<u><i>Successfully Forwarded</i></u>\n\n<b>Total Forwarded Files:-</b> <code>{files_count}</code> <b>Files</b>\n<b>Thanks For Using Me❤️</b>",
        reply_markup=reply_markup
    )
        

