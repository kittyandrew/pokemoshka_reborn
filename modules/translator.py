from utils.internet_apis import MyBingTranslator, GoogleAPI
from utils.voice_maker import make_voice
from telethon.tl.custom import Message
from error_logging import error_logger
from telethon import events, Button
from typing import Union

lang_list = list()
bing = MyBingTranslator(lang_list)
google = GoogleAPI(lang_list)

async def init(bot):
    @bot.on(events.NewMessage(pattern=r"^\.tr(\s)?([a-z][a-z])?(-[a-z][a-z])?"))
    @error_logger
    async def translate_handler(event:Union[Message, events.NewMessage.Event]):
        replied_to:Message = await event.get_reply_message()
        if replied_to:
            _to_lang = event.pattern_match.group(2)
            if not _to_lang:
                _to_lang = "uk"
            else:
                _to_lang.strip()

            if replied_to.raw_text:
                result = google.google_translate(replied_to.raw_text, target=_to_lang)
                try_again_button = Button.inline("Спробувати ще раз..", f"try again|{replied_to.id}|{replied_to.chat_id}|{_to_lang}".encode("utf-8"))
                voice_button = Button.inline("Озвучити", f"make voice|{replied_to.id}|{replied_to.chat_id}|{_to_lang}".encode("utf-8"))
                buttons = [[try_again_button], [voice_button]]
                await replied_to.reply(result, buttons=buttons)
        else:
            try:
                _from_lang = event.pattern_match.group(2)
            except:
                _from_lang = None
            try:
                _to_lang = event.pattern_match.group(4).replace("-", "")
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
        elif "make voice" in data:
            _, _id, _chat, _to_lang = data.split("|")
            msg = await bot.get_messages(int(event.chat_id), ids=event.message_id)
            if msg.text:
                edited_text = google.chop(msg.text)
                voice_file = make_voice(edited_text, _to_lang)
                file = await bot.upload_file(voice_file)
                await bot.send_file(int(_chat), file, voice_note=True, reply_to=event.message_id)
                await event.edit(buttons=Button.clear())

    @bot.on(events.NewMessage(pattern=r"^(/voice|/voice@pokemonchik_bot)$"))
    @error_logger
    async def to_voice(event):
        msg = await event.get_reply_message()
        if msg:
            if msg.text:
                lang = google.detect_language(msg.text)
                edited_text = google.chop(msg.text)
                voice_file = make_voice(edited_text, lang)
                file = await bot.upload_file(voice_file)
                await bot.send_file(event.chat, file, voice_note=True, reply_to=event)