from telethon.tl.custom import Message
from error_logging import error_logger
from telethon import events, Button
from typing import Union
import fuckit
import time

chats = {}
MSG = \
"""Author: `Andrew Pythonista`
`username:` @kitty_andrew
`github:` [kittyandrew](https://www.github.com/kittyandrew)"""

async def init(bot):
    @bot.on(events.NewMessage(pattern=r"^(/author|/author@pokemonchik_bot)$"))
    @error_logger
    async def author_handler(event):
        if chats.get(event.chat_id, None):
            delta = chats[event.chat_id] - time.time()
            if delta > 10:
                await event.respond(MSG, link_preview=False)
        else:
            chats[event.chat_id] = time.time()
            await event.respond(MSG, link_preview=False)

        with fuckit:
            await event.delete()