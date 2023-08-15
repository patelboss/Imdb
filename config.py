import re
import os
import logging

API_HASH = os.environ.get("API_HASH", "")
API_ID = os.environ.get("API_ID", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_SESSION = os.environ.get("BOT_SESSION", "bot")
CAPTION = os.environ.get("CAPTION", "")
FROM_CHANNEL = os.environ.get("FROM_CHANNEL", None)
FILTER_TYPE = os.environ.get("FILTER_TYPE", "empty")
OWNER_ID = os.environ.get("OWNER_ID", "1169128654")
LIMIT = os.environ.get("LIMIT", "2500000")
SKIP_NO = os.environ.get("SKIP_NO", "0")
SESSION = os.environ.get("SESSION")
TO_CHANNEL = os.environ.get("TO_CHANNEL", "")
PORT = os.environ.get("PORT", "8080")

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
