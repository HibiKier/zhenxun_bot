import random

from services import logger
from utils.image_utils import get_img_hash
from ._rule import check
from ._model import WordBank
from configs.path_config import DATA_PATH, TEMP_PATH
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from utils.utils import get_message_img, get_message_text, get_message_at
from nonebot import on_message
from utils.http_utils import AsyncHttpx

__zx_plugin_name__ = "词库问答回复操作 [Hidden]"

data_dir = DATA_PATH / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)

message_handle = on_message(priority=6, block=True, rule=check)


@message_handle.handle()
async def _(event: MessageEvent):
    text = get_message_text(event.message)
    img = get_message_img(event.message)
    at = get_message_at(event.message)
    problem = None
    if not text and img and len(img) == 1:
        rand = random.randint(1, 10000)
        if await AsyncHttpx.download_file(img[0], TEMP_PATH / f"{event.user_id}_{rand}_word_bank.jpg"):
            problem = str(get_img_hash(TEMP_PATH / f"{event.user_id}_{rand}_word_bank.jpg"))
    elif at:
        temp = ''
        for seg in event.message:
            if seg.type == 'at':
                temp += f"[at:{seg.data['qq']}]"
            else:
                temp += seg
        problem = temp
    elif text:
        problem = text
    if problem:
        if msg := await WordBank.get_answer(event, problem):
            await message_handle.send(msg)
            logger.info(
                f"(USER {event.user_id}, GROUP "
                f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 触发词条 {problem}"
            )



