from pyrogram import Client
import tgcrypto
from config import *

with Client(':memory:', api_id=API_KEY, api_hash=API_HASH) as app:
    print(app.export_session_string())
    print("""
Congrats! 
Also Session String Saved to Your SAVED MESSAGES""")
    session = app.export_session_string()
    a = app.send_message("me", "`{}`".format(app.export_session_string()))
    app.send_message(
        chat_id=a.chat.id,
        text="""**👆 Here's your requested User Session String for Bot**
 """,
        reply_to_message_id=a.message_id)
