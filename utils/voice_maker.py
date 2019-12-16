from telethon.tl.types import DocumentAttributeAudio
from telethon.tl.custom import Message
from telethon import events
from io import BytesIO
from gtts import gTTS
import asyncio
import aiohttp
import io


class CgTTS(gTTS):

    def save(self, file):
        self.write_to_fp(file)

class TTS_GEN:

    def __init__(self):
        pass

    def __call__(self, text, lang):
        tmp_file = BytesIO()
        tmp_voice = CgTTS(text=text, lang=lang)
        tmp_voice.save(tmp_file)
        return tmp_file.getvalue()

voice_factory = TTS_GEN()

def make_voice(text, language):

    voice = voice_factory(text, language)
    voice = io.BytesIO(voice)
    voice.name = 'translation.ogg'

    # Adding some missing info about audio
    # TODO: Make telegram show audio length
    # TODO: and add a proper waveform
    attributes = None

    return voice

