import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "")

API_HASH = os.environ.get("API_HASH", "")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

FORCE_SUB = os.environ.get("FORCE_SUB", "") 

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()]

DATABASE_URI = os.environ.get("DATABASE_URI", "")

MY_CHANNEL = os.environ.get("MY_CHANNEL", "")

PORT = os.environ.get("PORT", "8080")
