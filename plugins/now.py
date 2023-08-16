from pyrogram import Client, filters
import asyncio
import logging
from config import *

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log when the bot starts
logging.info("Bot started. Listening for commands and messages...")

copied_message_count = 0
forwarding_active = False

@Client.on_message(filters.command("run") & filters.private)
async def start_forwarding(client, message):
    global forwarding_active
    if forwarding_active:
        await client.send_message(message.chat.id, "Forwarding is already active.")
    else:
        forwarding_active = True
        await forward_messages(client)

@Client.on_message(filters.chat(FROM_CHANNEL) & filters.text)
async def forward_messages(client, message):
    global copied_message_count, forwarding_active
    if forwarding_active:
        copied_message_count += 1

        caption = message.caption if message.caption else None

        await client.send_message(TO_CHANNEL, text=message.text, reply_to_message_id=message.message_id, caption=caption)

@Client.on_message(filters.command("count") & filters.private)
def show_copied_message_count(client, message):
    global copied_message_count
    client.send_message(message.chat.id, f"Copied {copied_message_count} messages so far.")

async def forward_messages(client):
    global forwarding_active
    try:
        async for message in client.iter_history(FROM_CHANNEL):
            if not forwarding_active:
                break

            if message.text:
                caption = message.caption if message.caption else None
                await client.send_message(TO_CHANNEL, text=message.text, caption=caption)

            elif message.media:
                caption = message.caption if message.caption else None
                await client.send_media(TO_CHANNEL, media=message.media, caption=caption)
    finally:
        forwarding_active = False
