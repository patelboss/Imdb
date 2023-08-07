import re
from os import environ


# Bot information
BOT_TOKEN = environ['BOT_TOKEN']
SESSION = environ.get('SESSION', 'IMDB_bot')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
