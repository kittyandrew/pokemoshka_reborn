from telethon.tl.custom import Message
from error_logging import error_logger
from telethon import events, Button
from bs4 import BeautifulSoup
from typing import Union
import aiohttp
import asyncio
import fuckit

class Game:
    def __init__(self):
        self.user_id:int = None
        self.slovo:str = None
        self.timeout:bool = False
        self.owner:int = None

    async def new_game(self, user_id):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://sum.in.ua/random") as response:
                bs = BeautifulSoup(await response.text(), "lxml")
                slovo_div = bs.find("div", {"id": "tlum"})
                slovo = slovo_div.find("strong")
                self.slovo = slovo.text
                self.user_id = user_id
                return self

    def guess(self, word, user_id):
        result = (word == self.slovo)
        if result:
            self.owner = user_id
        return result

    def finish(self):
        self.user_id:str = None
        self.slovo:str = None
        self.timeout:bool = False

games = {}

async def _new_game(event, sender):
    if games.get(event.chat_id, None):
        await (games[event.chat_id]).new_game(sender.id)
    else:
        games[event.chat_id] = await Game().new_game(sender.id)

    buttons = [[Button.inline("Переглянути слово", f"check word|{sender.id}".encode("utf-8"))],
               [Button.inline("Замінити слово", f"change word|{sender.id}".encode("utf-8"))]]
    await event.respond(f"{sender.first_name} має пояснити слово за 2 хвилини",
                        buttons=buttons)
    #
    await asyncio.sleep(120)
    games[event.chat_id].timeout = True


async def init(bot):
    @bot.on(events.NewMessage(pattern=r"^(/krokodil|/krokodil@pokemonchik_bot)$"))
    @error_logger
    async def new_game(event:Union[Message, events.NewMessage.Event]):
        if games.get(event.chat_id, None):
            if games[event.chat_id].timeout or (not games[event.chat_id].owner and not games[event.chat_id].slovo):
                sender = await event.get_sender()
                await _new_game(event, sender)
        else:
            sender = await event.get_sender()
            await _new_game(event, sender)

        with fuckit:
            await event.delete()

    @bot.on(events.CallbackQuery())
    @error_logger
    async def krokodil_button(event):
        data: str = event.data.decode("utf-8")
        _, *_id = data.split("|")
        with fuckit:
            _id = int(_id[0])

        if event.sender_id == _id:
            if "check word" in data:
                await event.answer(games[event.chat_id].slovo, alert=True)
            elif "change word" in data:
                await (games[event.chat_id]).new_game(_id)
                await event.answer(games[event.chat_id].slovo, alert=True)
        elif "new game" in data:
            sender = await event.get_sender()
            if games.get(event.chat_id, None):
                if games[event.chat_id].owner and games[event.chat_id].owner != _id:
                    await event.answer("У переможця є 15 секунд, щоб розпочати гру.", alert=True)
                else:
                    await _new_game(event, sender)
            else:
                await _new_game(event, sender)
        else:
            await event.answer("Ти впевнений, що це для тебе?", alert=True)

    @bot.on(events.NewMessage())
    @error_logger
    async def new_game(event: Union[Message, events.NewMessage.Event]):
        if event.chat_id in games:
            if games[event.chat_id].guess(event.text.lower(), event.sender_id):
                sender = await event.get_sender()
                slovo = games[event.chat_id].slovo
                buttons = Button.inline("Нова гра", f"new game|{sender.id}".encode("utf-8"))
                if games[event.chat_id].user_id != event.sender_id:
                    await event.respond(f"{sender.first_name} вгадав слово {slovo}!", buttons=buttons)
                else:
                    await event.respond(f"{sender.first_name} вгадав своє ж слово {slovo}.. (точно геній)", buttons=buttons)
                games[event.chat_id].finish()
                # Give winner 15 seconds to win to start
                await asyncio.sleep(15)
                games[event.chat_id].owner = None