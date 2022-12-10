import imagehash
from PIL import Image
from io import BytesIO
from services.log import logger

from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageEvent, Bot

from utils.utils import get_message_text, get_message_img, get_message_at
from ._model import WordBank
from utils.http_utils import AsyncHttpx


async def check(bot: Bot, event: MessageEvent, state: T_State) -> bool:
    text = get_message_text(event.message)
    img = get_message_img(event.message)
    at = get_message_at(event.message)
    problem = text
    if not text and len(img) == 1:
        try:
            r = await AsyncHttpx.get(img[0])
            problem = str(imagehash.average_hash(Image.open(BytesIO(r.content))))
        except Exception as e:
            logger.warning(f"word_bank rule 获取图片失败 {type(e)}：{e}")
    if at:
        temp = ''
        for seg in event.message:
            if seg.type == 'at':
                temp += f"[at:{seg.data['qq']}]"
            elif seg.type == 'text':
                temp += seg.data["text"]
        problem = temp
    if event.to_me and bot.config.nickname:
        if str(event.original_message).startswith("[CQ:at"):
            problem = f"[at:{bot.self_id}]" + problem
        else:
            if problem and bot.config.nickname:
                nickname = [nk for nk in bot.config.nickname if str(event.original_message).startswith(nk)]
                problem = nickname[0] + problem if nickname else problem
    if problem and (await WordBank.check(event, problem) is not None):
        state["problem"] = problem
        return True
    return False
