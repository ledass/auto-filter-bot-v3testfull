#!/usr/bin/env python3
import logging
import logging.config
import time
import asyncio
import pytz
from datetime import datetime

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from plugins import Media
from config import SESSION, API_ID, API_HASH, BOT_TOKEN
import pyromod.listen

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)

class Bot(Client):
    def __init__(self):
        super().__init__(
            session_name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        self.username = '@' + me.username
        print(f"{me.first_name} with Pyrogram v{__version__} (Layer {layer}) started as {me.username}.")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")

async def wait_for_time_sync():
    now = datetime.now(pytz.utc)
    if abs(time.time() - now.timestamp()) > 10:
        print("⏳ Time out of sync. Sleeping for 30 seconds to sync...")
        await asyncio.sleep(30)

asyncio.get_event_loop().run_until_complete(wait_for_time_sync())

app = Bot()
app.run()
