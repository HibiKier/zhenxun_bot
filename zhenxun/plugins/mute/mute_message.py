from nonebot import on_message
from nonebot.adapters import Bot
from nonebot_plugin_alconna import Image as alcImage
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import NICKNAME
from zhenxun.services.log import logger
from zhenxun.utils.image_utils import get_download_image_hash
from zhenxun.utils.platform import PlatformUtils

from ._data_source import mute_manage

_matcher = on_message(priority=1, block=False)


@_matcher.handle()
async def _(bot: Bot, session: EventSession, message: UniMsg):
    group_id = session.id2
    if not session.id1 or not group_id:
        return
    plain_text = message.extract_plain_text()
    image_list = [m.url for m in message if isinstance(m, alcImage) and m.url]
    img_hash = ""
    for url in image_list:
        img_hash += await get_download_image_hash(url, "_mute_")
    _message = plain_text + img_hash
    if duration := mute_manage.add_message(session.id1, group_id, _message):
        try:
            await PlatformUtils.ban_user(bot, session.id1, group_id, duration)
            await Text(f"检测到恶意刷屏，{NICKNAME}要把你关进小黑屋！").send(
                at_sender=True
            )
            mute_manage.reset(session.id1, group_id)
            logger.info(f"检测刷屏 被禁言 {duration} 分钟", "禁言检查", session=session)
        except Exception as e:
            logger.error("禁言发送错误", "禁言检测", session=session, e=e)
