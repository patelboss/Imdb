from pyrogram import Client, filters
import re
from imdb import IMDb
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, DATABASE_URI, BOT_TOKEN
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info("Bot started. Listening for commands and messages...")


# Command handler for /start
@Client.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! I'm beta type of @Rashmika_mandanana_bot\n Not Beta I am beta of her. 😂\n I am restricted from public use so try on your own risk 🙏🏻")

# Command handler for /help
@Client.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text("If You have Permission to use me. then do 🙏🏻.")

# Function to perform IMDb search and return results as InlineKeyboardMarkup
def perform_imdb_search(search_text):
    logging.info("searching.")
    
    ia = IMDb()
    search_results = ia.search_movie(search_text)

    if search_results:
        keyboard = []
        for i, result in enumerate(search_results[:10], start=1):
            title = result['title']
            year = result.get('year', 'N/A')
            button_text = f"{i}. {title} - {year}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=title)])

        return InlineKeyboardMarkup(keyboard)
    else:
        return None
        
     
# Message handler for regular text messages in groups
@Client.on_message(filters.group & filters.text)
async def reply_to_text(client, message):
    logging.info("Received search text: %s", message.text)
    
    search_text = message.text

    # Count the number of words in the search_text
    word_count = len(re.findall(r'\w+', search_text))
    logging.info("Word count: %d", word_count)

    if word_count < 20:
        logging.info("Performing IMDb search for: %s", search_text)
        inline_keyboard = perform_imdb_search(search_text)

        if inline_keyboard:
            logging.info("Sending paginated results...")
            await send_paginated_results(message.chat.id, inline_keyboard)
        else:
            # IMDb search not found, provide a suggestion
            suggestion_message = "No results found for '{}'.".format(search_text)
            logging.info(suggestion_message)
            await message.reply_text(suggestion_message)

# Callback handler for inline keyboard buttons
@Client.on_callback_query()
async def callback_query_handler(client, query):
    logging.info("Callback query received.")
    file_id = query.data  # Get the selected file ID (_id)

    try:
        # Retrieve the file details from the database using the file_id
        mongo_client = MongoClient(DATABASE_URI)
        db = mongo_client['TelegramBot']
        collection = db['TelegramBot']

        file_details = collection.find_one({"_id": file_id})
        if file_details:
            file_name = file_details['file_name']
            mime_type = file_details['mime_type']
            file_caption = file_details['caption']

            # Send the file using its file ID (_id)
            await query.message.reply_document(file_id, caption=file_caption, filename=file_name, mime_type=mime_type)
        else:
            reply_message = f"No file found for '{file_id}'."
            await query.message.edit_text(reply_message)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Callback handler for pagination buttons
@Client.on_callback_query(filters.regex(r'^(prev|next)_\d+$'))
async def pagination_callback_handler(client, query):
    logging.info("next")


    callback_data = query.data
    action, page_num = callback_data.split('_')

    try:
        page_num = int(page_num)
        chat_id = query.message.chat.id

        if action == 'prev' and page_num > 0:
            page_num -= 1
        elif action == 'next':
            page_num += 1

        # Retrieve the original inline keyboard and update the pagination buttons
        inline_keyboard = query.message.reply_markup
        updated_keyboard = update_pagination_buttons(inline_keyboard, page_num)
        
        await query.message.edit_reply_markup(updated_keyboard)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

async def update_pagination_buttons(inline_keyboard, page_num, chat_id):
    logging.info("update paginated button")

    results_per_page = 10
    num_results = len(inline_keyboard.inline_keyboard) - 1  # Subtract 1 for pagination buttons
    num_pages = (num_results + results_per_page - 1) // results_per_page

    start_idx = page_num * results_per_page
    end_idx = min(start_idx + results_per_page, num_results)
    page_keyboard = inline_keyboard.inline_keyboard[start_idx:end_idx]

    # Add pagination buttons (previous and next)
    pagination_buttons = []
    if page_num > 0:
        pagination_buttons.append(InlineKeyboardButton("Previous", callback_data=f"prev_{page_num}"))
    if page_num < num_pages - 1:
        pagination_buttons.append(InlineKeyboardButton("Next", callback_data=f"next_{page_num}"))
    
    page_keyboard.append(pagination_buttons)

    updated_keyboard = InlineKeyboardMarkup(page_keyboard)
    await send_paginated_results(chat_id, updated_keyboard)

async def send_paginated_results(chat_id, inline_keyboard):
    logging.info("send paginated results")
    results_per_page = 10
    num_results = len(inline_keyboard.inline_keyboard)
    num_pages = (num_results + results_per_page - 1) // results_per_page

    # Send the first page of results
    await bot.send_message(chat_id, "Here are the search results:", reply_markup=inline_keyboard)
