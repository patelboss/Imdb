#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Dark Angel

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from config import *
from plugins.translation import Translation
from user import User
from pyrogram import errors

FROM = FROM_CHANNEL
TO = TO_CHANNEL
FILTER = FILTER_TYPE

@Client.on_message(filters.private & filters.command(["run"]))
async def run(bot, message):
    if str(message.from_user.id) not in OWNER_ID:
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
    async for message in bot.User.search_messages(chat_id=FROM, offset=SKIP_NO, limit=LIMIT, filter=FILTER):
        try:
            if message.video:
                file_name = message.video.file_name
            elif message.document:
                file_name = message.document.file_name
            elif message.audio:
                file_name = message.audio.file_name
            else:
                file_name = None
            await bot.copy_message(chat_id=TO, from_chat_id=FROM, message_id=message.message_id )
            files_count += 1
            await asyncio.sleep(1)
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
        


@Client.on_message()
def forward_old_messages(message):
  if message.chat.type == 'private' and message.text == 'forward':
    source_chat_id = FROM_CHANNEL
    target_chat_id = TO_CHANNEL
    start_message_id = 2
    end_message_id = 19

    reply_text = f'Forwarding {end_message_id - start_message_id + 1} messages from {source_chat_id} to {target_chat_id}'
    bot.send_message(
      message.chat.id,
      reply_text
    )

    for message in bot.iter_messages(
        source_chat_id,
        from_message_id=start_message_id,
        to_message_id=end_message_id
    ):
      bot.forward_message(
        target_chat_id,
        message.chat.id,
        message.message_id
      )
