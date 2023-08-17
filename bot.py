import logging
import logging.config
from pyrogram import Client, __version__
from config import *
from aiohttp import web
from plugins.web_support import web_server
from user import User
from pyrogram.raw import functions
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class Bot(Client):
    USER: User = @Lucifer_film_bot
    USER_ID: int = OWNER_ID

    def __init__(self):
        super().__init__(
            BOT_SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
       await super().start()
       me = await self.get_me()
       self.mention = me.mention
       self.username = me.username
       app = web.AppRunner(await web_server())
       await app.setup()
       bind_address = "0.0.0.0"
       await web.TCPSite(app, bind_address, PORT).start()
       logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")

    async def stop(self, *args):
      await super().stop()
      logging.info("Bot Stopped 🙄")
