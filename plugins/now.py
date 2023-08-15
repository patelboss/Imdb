#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Dark Angel

import os
import re
import sys
import asyncio
from plugins.translation import Translation
from pyrogram import Client, filters, __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import logging  # Import the logging module
from config import *
from pyrogram.errors import FloodWait

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    logger.info("Received /start command")
    buttons = [
        [InlineKeyboardButton('📜𝐒𝐮𝐩𝐩𝐨𝐫𝐭', url='https://t.me/Filmykeedha'),
         InlineKeyboardButton('𝐔𝐩𝐝𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥♻️', url='https://t.me/Filmykeedha')],
        [InlineKeyboardButton('💡𝐒𝐨𝐮𝐜𝐞𝐂𝐨𝐝𝐞💡', url='https://github.com/patelboss/File-Auto-Forword-Bot')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Translation.START_TXT.format(message.from_user.first_name),
    )



@Client.on_message(filters.private & filters.command(['help']))
async def help(client, message):
    logging.info("Received /help command")
    buttons = [[InlineKeyboardButton('𝐜𝐥𝐨𝐬𝐞 🔐', callback_data='close_btn')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Translation.HELP_TXT,
    )

@Client.on_message(filters.private & filters.command(['about']))
async def about(client, message):
    logging.info("Received /about command")
    buttons = [
        [InlineKeyboardButton('💡𝐒𝐨𝐮𝐜𝐞𝐂𝐨𝐝𝐞', url='https://github.com/patelboss/File-Auto-Forword-Bot'),
         InlineKeyboardButton('𝐜𝐥𝐨𝐬𝐞🔐', callback_data='close_btn')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Translation.ABOUT_TXT,
        disable_web_page_preview=True,
    )

@Client.on_message(filters.private & filters.command(["run"]))
async def run(bot, message):
    logging.info("Received /run command")
    
    # Check if user is in OWNER_ID list
    if str(message.from_user.id) not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    buttons = [[InlineKeyboardButton('🚫 𝐒𝐓𝐎𝐏', callback_data='stop_btn')]]
    reply_markup = InlineKeyboardMarkup(buttons)

    m = await bot.send_message(
        text="<i>File Forwarding Started😉 Join @filmykeedha</i>",
        reply_markup=reply_markup,
        chat_id=message.chat.id
    )

    files_count = 0
    async for message in bot.USER.search_messages(chat_id=FROM, offset=SKIP_NO, limit=LIMIT, filter=FILTER):
      if message.video or message.document or message.audio:
        try:
            if message.video:
                file_name = message.video.file_name
            elif message.document:
                file_name = message.document.file_name
            elif message.audio:
                file_name = message.audio.file_name
            else:
                file_name = None
            logging.info(f"Forwarding message with file: {file_name}")
            await bot.copy_message(
                chat_id=TO,
                from_chat_id=FROM,
                parse_mode="md",
                caption=Translation.CAPTION.format(file_name),
                message_id=message.message_id
            )

            files_count += 1
            await asyncio.sleep(1)

        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print(e)
            pass

    buttons = [[InlineKeyboardButton('📜 𝐔𝐩𝐝𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥', url='https://t.me/Filmykeedha')]]
    reply_markup = InlineKeyboardMarkup(buttons)

    await m.edit(
        text=f"<u><i>Successfully Forwarded</i></u>\n\n<b>Total Forwarded Files:-</b> <code>{files_count}</code> <b>Files</b>\n<b>Thanks For Using Me❤️</b>",
        reply_markup=reply_markup
    )


@Client.on_callback_query(filters.regex(r'^stop_btn$'))
async def stop_button(c: Client, cb: CallbackQuery):
    logging.info("Stop Button Callback")
    await cb.message.delete()
    await cb.answer()

    msg = await c.send_message(
        text="<i>Trying To Stop..... @filmykeedha</i>",
        chat_id=cb.message.chat.id
    )

    await asyncio.sleep(5)

    await msg.edit("<i>File Forwarding Stopped Successfully 👍 @filmykeedha</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close(bot, update):
    await update.answer()
    await update.message.delete()
