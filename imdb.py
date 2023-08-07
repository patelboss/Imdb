import logging
from pyrogram import Client, __version__
import re
from imdb import IMDb

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a Pyrogram client
app = Client("my_bot")

# Define the on_message event handler
@app.on_message()
async def handle_message(client, message):
    if message.text:
        content = message.text

        # Extract text between $ and & using regular expressions
        match = re.search(r'\$(.*?)\&', content)
        if match:
            search_text = match.group(1)

            # Search IMDb using 'search_text' and retrieve results
            ia = IMDb()
            search_results = ia.search_movie(search_text)

            if search_results:
                # Get the first three search results
                first_three_results = search_results[:3]
                reply_message = f"IMDb search results for '{search_text}':\n"
                for result in first_three_results:
                    title = result['title']
                    release_date = result.get('release date', 'N/A')
                    release_year = result.get('year', 'N/A')

                    if release_date != 'N/A':
                        release_info = f"Release Date: {release_date}"
                    else:
                        release_info = f"Release Year: {release_year}"

                    reply_message += f"\nTitle: {title}\n{release_info}"

                # Send IMDb search results
                await client.send_message(chat_id=message.chat.id, text=reply_message)
            else:
                # No search results found, send a message indicating no queries are related
                await client.send_message(chat_id=message.chat.id, text=f"No Queries Related {search_text}")

# Start the Pyrogram client
app.run()
