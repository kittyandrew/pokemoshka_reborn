from telethon import TelegramClient
import modules
import config as c
import asyncio

class TelethonManager:

    def __init__(self, loop=None):
        self.loop = loop
        self.client = TelegramClient(session=f'pokemoshka', api_hash="a3406de8d171bb422bb6ddf3bbd800e2", api_id="94575", loop=self.loop)

    def start(self):

        ## register handlers
        modules.init(self.client)

        ## register background events

        # Start
        self.client.start(bot_token=c.TOKEN)
        self.client.run_until_disconnected()

if __name__ == "__main__":
    TelethonManager().start()
