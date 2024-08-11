from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Option,
    on_alconna,
    store_true,
)
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils

from ._data_source import uid_pid_exists
from ._model.pixiv import Pixiv
from ._model.pixiv_keyword_user import PixivKeywordUser

__plugin_meta__ = PluginMetadata(
    name="PIX添加",
    description="PIX关键词/UID/PID添加管理",
    usage="""
    指令：
        添加pix关键词 [Tag]: 添加一个pix搜索收录Tag
        pix添加 uid [uid]: 添加一个pix搜索收录uid
        pix添加 pid [pid]: 添加一个pix收录pid
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
    ).dict(),
)

_add_matcher = on_alconna(
    Alconna("添加pix关键词", Args["keyword", str]), priority=5, block=True
)

_uid_matcher = on_alconna(
    Alconna(
        "pix添加",
        Args["add_type", ["uid", "pid"]]["id", str],
        Option("-f", action=store_true, help_text="强制收录不检查是否存在"),
    ),
    priority=5,
    block=True,
)

_black_matcher = on_alconna(
    Alconna("添加pix黑名单", Args["pid", str]), priority=5, block=True
)


@_add_matcher.handle()
async def _(bot: Bot, session: EventSession, keyword: str, arparma: Arparma):
    group_id = session.id3 or session.id2 or -1
    if not await PixivKeywordUser.exists(keyword=keyword):
        await PixivKeywordUser.create(
            user_id=str(session.id1),
            group_id=str(group_id),
            keyword=keyword,
            is_pass=str(session.id1) in bot.config.superusers,
        )
        text = f"已成功添加pixiv搜图关键词：{keyword}"
        if session.id1 not in bot.config.superusers:
            text += "，请等待管理员通过该关键词！"
        await MessageUtils.build_message(text).send(reply_to=True)
        logger.info(
            f"添加了pixiv搜图关键词: {keyword}", arparma.header_result, session=session
        )
    else:
        await MessageUtils.build_message(f"该关键词 {keyword} 已存在...").send()


@_uid_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma, add_type: str, id: str):
    group_id = session.id3 or session.id2 or -1
    exists_flag = True
    if arparma.find("f") and session.id1 in bot.config.superusers:
        exists_flag = False
    word = None
    if add_type == "uid":
        word = f"uid:{id}"
    else:
        word = f"pid:{id}"
        if await Pixiv.get_or_none(pid=int(id), img_p="p0"):
            await MessageUtils.build_message(f"该PID：{id}已存在...").finish(
                reply_to=True
            )
    if not await uid_pid_exists(word) and exists_flag:
        await MessageUtils.build_message(
            "画师或作品不存在或搜索正在CD，请稍等..."
        ).finish(reply_to=True)
    if not await PixivKeywordUser.exists(keyword=word):
        await PixivKeywordUser.create(
            user_id=session.id1,
            group_id=str(group_id),
            keyword=word,
            is_pass=session.id1 in bot.config.superusers,
        )
        text = f"已成功添加pixiv搜图UID/PID：{id}"
        if session.id1 not in bot.config.superusers:
            text += "，请等待管理员通过该关键词！"
        await MessageUtils.build_message(text).send(reply_to=True)
    else:
        await MessageUtils.build_message(f"该UID/PID：{id} 已存在...").send()


@_black_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma, pid: str):
    img_p = ""
    if "p" in pid:
        img_p = pid.split("p")[-1]
        pid = pid.replace("_", "")
        pid = pid[: pid.find("p")]
    if not pid.isdigit:
        await MessageUtils.build_message("PID必须全部是数字！").finish(reply_to=True)
    if not await PixivKeywordUser.exists(
        keyword=f"black:{pid}{f'_p{img_p}' if img_p else ''}"
    ):
        await PixivKeywordUser.create(
            user_id=114514,
            group_id=114514,
            keyword=f"black:{pid}{f'_p{img_p}' if img_p else ''}",
            is_pass=session.id1 in bot.config.superusers,
        )
        await MessageUtils.build_message(f"已添加PID：{pid} 至黑名单中...").send()
        logger.info(
            f" 添加了pixiv搜图黑名单 PID:{pid}", arparma.header_result, session=session
        )
    else:
        await MessageUtils.build_message(
            f"PID：{pid} 已添加黑名单中，添加失败..."
        ).send()
