import random

from nonebot.adapters.onebot.v11 import MessageEvent

from configs.path_config import TEMP_PATH
from utils.image_utils import get_img_hash
from utils.utils import get_message_text, get_message_img, get_message_at
from ._model import WordBank
from utils.http_utils import AsyncHttpx


async def check(event: MessageEvent) -> bool:
    text = get_message_text(event.message)
    img = get_message_img(event.message)
    at = get_message_at(event.message)
    rand = random.randint(1, 100)
    problem = text
    if not text and len(img) == 1:
        if await AsyncHttpx.download_file(img[0], TEMP_PATH / f"{event.user_id}_{rand}_word_bank_check.jpg"):
            problem = str(get_img_hash(TEMP_PATH / f"{event.user_id}_{rand}_word_bank_check.jpg"))
    if at:
        temp = ''
        for seg in event.message:
            if seg.type == 'at':
                temp += f"[at:{seg.data['qq']}]"
            else:
                temp += seg
        problem = temp
    if problem:
        return await WordBank.check(event, problem) is not None
    return False
