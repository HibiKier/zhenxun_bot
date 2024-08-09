from typing import List

from nonebot import on_message
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import NICKNAME, Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.models.friend_user import FriendUser
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.services.log import logger
from zhenxun.utils.depends import UserName
from zhenxun.utils.message import MessageUtils

from .data_source import get_chat_result, hello, no_result

__plugin_meta__ = PluginMetadata(
    name="AI",
    description="屑Ai",
    usage=f"""
    与{NICKNAME}普普通通的对话吧！
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        configs=[
            RegisterConfig(
                module="alapi",
                key="ALAPI_TOKEN",
                value=None,
                help="在 https://admin.alapi.cn/user/login 登录后获取token",
            ),
            RegisterConfig(key="TL_KEY", value=[], help="图灵Key", type=List[str]),
            RegisterConfig(
                key="ALAPI_AI_CHECK",
                value=False,
                help="是否检测青云客骂娘回复",
                default_value=False,
                type=bool,
            ),
            RegisterConfig(
                key="TEXT_FILTER",
                value=["鸡", "口交"],
                help="文本过滤器，将敏感词更改为*",
                type=List[str],
            ),
        ],
    ).dict(),
)


ai = on_message(rule=to_me(), priority=998)


@ai.handle()
async def _(message: UniMsg, session: EventSession, uname: str = UserName()):
    if not message or message.extract_plain_text() in [
        "你好啊",
        "你好",
        "在吗",
        "在不在",
        "您好",
        "您好啊",
        "你好",
        "在",
    ]:
        await hello().finish()
    if not session.id1:
        await Text("用户id不存在...").finish()
    gid = session.id3 or session.id2
    if gid:
        nickname = await GroupInfoUser.get_user_nickname(session.id1, gid)
    else:
        nickname = await FriendUser.get_user_nickname(session.id1)
    if not nickname:
        nickname = uname
    result = await get_chat_result(message, session.id1, nickname)
    logger.info(f"问题：{message} ---- 回答：{result}", "ai", session=session)
    if result:
        result = str(result)
        for t in Config.get_config("ai", "TEXT_FILTER"):
            result = result.replace(t, "*")
        await MessageUtils.build_message(result).finish()
    else:
        await no_result().finish()
