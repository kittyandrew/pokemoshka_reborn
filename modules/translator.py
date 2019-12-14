from utils.internet_apis import MyBingTranslator, GoogleAPI
from telethon.tl.custom import Message
from error_logging import error_logger
from telethon import events, Button
from typing import Union

bing = MyBingTranslator()
google = GoogleAPI()

async def init(bot):
    @bot.on(events.NewMessage(pattern=r"^\.tr( [a-z]{:2}(\-)?)?([a-z]{:2})?"))
    @error_logger
    async def translate_handler(event:Union[Message, events.NewMessage.Event]):
        replied_to:Message = await event.get_reply_message()

        if replied_to:
            _to_lang = event.pattern_match.group(1)
            if not _to_lang:
                _to_lang = "uk"
            else:
                _to_lang.strip("")

            if replied_to.raw_text:
                result = google.google_translate(replied_to.raw_text, target=_to_lang)
                buttons = Button.inline("Спробувати ще раз..", f"try again|{replied_to.id}|{replied_to.chat_id}|{_to_lang}".encode("utf-8"))
                await replied_to.reply(result, buttons=buttons)
        else:
            try:
                _from_lang = event.pattern_match.group(1)
            except:
                _from_lang = None
            try:
                _to_lang = event.pattern_match.group(3)
            except:
                _to_lang = None

    @bot.on(events.CallbackQuery())
    @error_logger
    async def button_pressed(event):
        data:str = event.data.decode("utf-8")

        if "try again" in data:
            _, _id, _chat, _to_lang = data.split("|")
            msg = await bot.get_messages(int(_chat), ids=int(_id))
            if msg.raw_text:
                result = bing.translate(msg.raw_text, target=_to_lang, tell_input_lang=True)
                await event.edit(result, buttons=Button.clear())