import imagehash
from PIL import Image
from io import BytesIO
from httpx import TimeoutException

from nonebot.adapters.onebot.v11 import MessageEvent

from utils.utils import get_message_text, get_message_img, get_message_at
from ._model import WordBank
from utils.http_utils import AsyncHttpx


async def check(event: MessageEvent) -> bool:
    text = get_message_text(event.message)
    img = get_message_img(event.message)
    at = get_message_at(event.message)
    problem = text
    if not text and len(img) == 1:
        try:
            r = await AsyncHttpx.get(img[0])
            problem = str(imagehash.average_hash(Image.open(BytesIO(r.content))))
        except TimeoutException:
            pass
    if at:
        temp = ''
        for seg in event.message:
            if seg.type == 'at':
                temp += f"[at:{seg.data['qq']}]"
            elif isinstance(seg, str):
                temp += seg
            elif seg.type == 'text':
                temp += seg.data["text"]
        problem = temp
    if problem:
        return await WordBank.check(event, problem) is not None
    return False
