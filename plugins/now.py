#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Dark Angel

import os
import re
import sys
import asyncio
from plugins.translation import Translation
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import logging  # Import the logging module
from config import *


# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    logger.info("Received start command")
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
    buttons = [[InlineKeyboardButton('𝐜𝐥𝐨𝐬𝐞 🔐', callback_data='close_btn')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Translation.HELP_TXT,
    )

@Client.on_message(filters.private & filters.command(['about']))
async def about(client, message):
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



@Client.on_message(filters.private & filters.command("start_forward"))
def start_forward(client, message):
    global forwarding
    forwarding = True
    message.reply_text("Forwarding started! Send a message to be forwarded.")

forwarding = False
forwarded_count = 0

@Client.on_message(filters.private & ~filters.command("start_forward") & filters.reply & filters.text)
def forward_message(client, message):
    global forwarding, forwarded_count

    if forwarding:
        try:
            forwarded_message = client.forward_messages(chat_id=message.chat.id, from_chat_id=message.reply_to_message.forward_from_chat.id, message_ids=message.reply_to_message.message_id)
            forwarded_count += 1
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Stop Forwarding", callback_data="stop")]])
            message.reply_text(f"Message forwarded! Forwarded count: {forwarded_count}", reply_markup=reply_markup)
        except Exception as e:
            message.reply_text(f"Error: {e}")

@Client.on_callback_query(filters.regex("stop"))
def stop_forwarding(client, callback_query):
    global forwarding
    forwarding = False
    callback_query.answer("Forwarding stopped.")

@Client.on_message(filters.private & ~filters.command("start_forward") & ~filters.reply & filters.text)
def forward_old_message(client, message):
    global forwarding, forwarded_count

    if forwarding:
        try:
            forwarded_message = client.forward_messages(chat_id=message.chat.id, from_chat_id=message.chat.id, message_ids=message.message_id)
            forwarded_count += 1
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Stop Forwarding", callback_data="stop")]])
            message.reply_text(f"Old message forwarded! Forwarded count: {forwarded_count}", reply_markup=reply_markup)
        except Exception as e:
            message.reply_text(f"Error: {e}")
    
@Client.on_message(filters.private & filters.command("forward_all_media") & filters.user(OWNER_ID))
def start_forward_all_media(client, message):
    global forwarding, total_media_to_forward
    forwarding = True
    total_media_to_forward = 0
    message.reply_text("Forwarding all media started!")

@Client.on_message(filters.media & filters.chat(FROM))
def forward_media(client, message):
    global forwarding, forwarded_count, total_media_to_forward

    if forwarding:
        try:
            client.forward_messages(chat_id=TO, from_chat_id=FROM, message_ids=message.message_id)
            forwarded_count += 1
            total_media_to_forward -= 1
            if total_media_to_forward == 0:
                forwarding = False
                app.send_message(OWNER_ID, "All media have been successfully forwarded!")
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Stop Forwarding", callback_data="stop")]])
            message.reply_text(f"Media forwarded! Forwarded count: {forwarded_count}", reply_markup=reply_markup)
        except Exception as e:
            message.reply_text(f"Error: {e}")

# ...

@Client.on_callback_query(filters.regex("stop"))
def stop_forwarding(client, callback_query):
    global forwarding
    forwarding = False
    callback_query.answer("Forwarding stopped.")
