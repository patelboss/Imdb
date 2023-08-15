from pyrogram import Client, filters
from config import*


copied_message_count = 0

@app.on_message(filters.command("start"))
def start(client, message):
    global copied_message_count
    copied_message_count = 0
    messages = app.get_history(FROM_CHANNEL, limit=100)  # Adjust limit as needed
    for msg in messages:
        copy_message(client, msg)
    client.send_message(TO_CHANNEL, f"Copied {copied_message_count} messages from old history.")

@app.on_message(filters.chat(FROM_CHANNEL))
def copy_message(client, message):
    global copied_message_count
    copied_message_count += 1

    caption = None
    if message.caption:
        caption = message.caption

    if message.text:
        client.send_message(TO_CHANNEL, text=message.text, caption=caption)

    elif message.media:
        client.send_media(TO_CHANNEL, media=message.media, caption=caption)

@app.on_message(filters.command("count"))
def show_copied_message_count(client, message):
    global copied_message_count
    client.send_message(TO_CHANNEL, f"Copied {copied_message_count} messages so far.")
    
