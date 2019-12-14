from telethon import TelegramClient
import modules
import config as c
import asyncio

class TelethonManager:

    def __init__(self, loop=None):
        self.loop = loop
        self.client = TelegramClient(session=f'pokemoshka', api_hash="a02ade04381a34dfce7db9bf23e62926", api_id="906668", loop=self.loop)

    def start(self):

        ## register handlers
        modules.init(self.client)

        ## register background events

        # Start
        self.client.start(bot_token=c.TOKEN)
        self.client.run_until_disconnected()

if __name__ == "__main__":
    TelethonManager().start()