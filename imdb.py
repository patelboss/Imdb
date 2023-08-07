import os
import pyrogram

def get_api_id():
  """Get the api_id from the config.env file."""
  api_id = os.environ.get('API_ID')
  if api_id is None:
    raise Exception('API_ID not found in config.env file.')
  return api_id

def get_api_hash():
  """Get the api_hash from the config.env file."""
  api_hash = os.environ.get('API_HASH')
  if api_hash is None:
    raise Exception('API_HASH not found in config.env file.')
  return api_hash

def get_bot_token():
  """Get the bot token from the config.env file."""
  bot_token = os.environ.get('BOT_TOKEN')
  if bot_token is None:
    raise Exception('BOT_TOKEN not found in config.env file.')
  return bot_token

def get_imdb_top_three(query):
  """Get the top three IMDb results for the given query."""
  url = 'https://www.imdb.com/search/title?title_type=feature&sort=num_votes,desc&count=3&title=' + query
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'lxml')
  movies = soup.select('div.lister-item mode-advanced')
  results = []
  for movie in movies:
    title = movie.select('a.title')[0].text
    rating = movie.select('div.ratings-bar')[0].text
    release_date = movie.select('span.release_date')[0].text
    if release_date is None:
      release_date = re.search(r'\((.*?)\)', title).group(1)
    results.append({
      'title': title,
      'release_date': release_date,
      'rating': rating,
    })
  return results

@pyrogram.Client.on_message()
async def imdb_bot(client, message):
  query = message.text
  results = get_imdb_top_three(query)
  for result in results:
    await client.send_message(
      chat_id=message.chat.id,
      text='Title: {}\nRelease Date: {}\nRating: {}\n'.format(
        result['title'], result['release_date'], result['rating']))

if __name__ == '__main__':
  bot = pyrogram.Client('my_bot', api_id=get_api_id(), api_hash=get_api_hash(), bot_token=get_bot_token())
  bot.start()
  bot.run()
                        
