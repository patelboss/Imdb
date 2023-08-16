#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Dark Angel

from config import SESSION, API_HASH, API_ID
from config import LOGGER
from pyrogram import Client, __version__


class User(Client):
    def __init__(self):
        super().__init__(
               SESSION,
            api_hash=API_HASH,
            api_id=API_ID,
            workers=4
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        return (self, usr_bot_me.id)

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.SESSION")
