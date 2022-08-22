import imagehash
from PIL import Image
from io import BytesIO
from httpx import TimeoutException

from services import logger
from ._rule import check
from ._model import WordBank
from configs.path_config import DATA_PATH
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
        try:
            r = await AsyncHttpx.get(img[0])
            problem = str(imagehash.average_hash(Image.open(BytesIO(r.content))))
        except TimeoutException:
            logger.error(f"下载 {img[0]} 下载超时..")
    elif at:
        temp = ''
        for seg in event.message:
            if seg.type == 'at':
                temp += f"[at:{seg.data['qq']}]"
            elif isinstance(seg, str):
                temp += seg
            elif seg.type == 'text':
                temp += seg.data["text"]
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



