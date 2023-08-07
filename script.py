from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import re
import requests
from bs4 import BeautifulSoup

# Replace with your own bot token
TOKEN = 'your_bot_token_here'

def start(update, context):
    update.message.reply_text("Hello! I'm your IMDb bot. Send me a message with text between $ and & to get IMDb top three results.")

def get_imdb_results(update, context):
    message = update.message.text
    matches = re.findall(r'\$(.*?)\&', message)
    
    if not matches:
        return
    
    for query in matches:
        search_url = f"https://www.imdb.com/find?q={query}&s=tt&ttype=ft&ref_=fn_ft"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = soup.find_all("td", class_="result_text")
        
        if not results:
            continue
        
        for i, result in enumerate(results[:3]):
            title = result.a.get_text()
            href = result.a['href']
            imdb_url = f"https://www.imdb.com{href}"
            
            details_response = requests.get(imdb_url)
            details_soup = BeautifulSoup(details_response.content, 'html.parser')
            
            try:
                release_date = details_soup.find("a", title="See more release dates").get_text(strip=True)
            except AttributeError:
                release_date = details_soup.find("span", class_="nobr").get_text(strip=True)
            
            rating = details_soup.find("span", itemprop="ratingValue").get_text(strip=True)
            
            reply_text = f"Top {i + 1}:\nTitle: {title}\nRelease Date: {release_date}\nRating: {rating}\nIMDb URL: {imdb_url}"
            
            if update.message.chat.type == "group" or update.message.chat.type == "supergroup":
                context.bot.send_message(update.message.chat.id, reply_text)
            elif update.message.chat.type == "private":
                update.message.reply_text(reply_text)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    imdb_handler = MessageHandler(Filters.text & ~Filters.command, get_imdb_results)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(imdb_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
