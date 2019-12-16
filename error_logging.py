from telethon.tl.custom import Message
from telethon import events
from typing import Union
import functools
import logging
import fuckit

ERROR = 10
FATAL_ERROR = 20

logger = logging.getLogger(__name__)
fh = logging.FileHandler('logging.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)

def error_logger(func, importance=10):

    if importance <= 10:
        @functools.wraps(func)
        async def wrapped(event:Union[Message, events.NewMessage.Event]):
            try:
                await func(event)
            except events.StopPropagation as sp:
                raise sp
            except Exception as e:
                with fuckit:
                    log_msg = f"Ой-ой!```\nHandler: {func.__name__}\n\n{(e.__class__.__name__)}: {e}```"
                    await event.reply(log_msg)
                    logger.log(logging.ERROR, log_msg)

    else:
        raise NotImplementedError("There is no such logging method yet")
    return wrapped