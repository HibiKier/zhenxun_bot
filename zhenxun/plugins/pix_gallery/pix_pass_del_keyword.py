from nonebot.adapters import Bot
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    At,
    Match,
    Option,
    on_alconna,
    store_true,
)
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

from ._data_source import remove_image
from ._model.pixiv import Pixiv
from ._model.pixiv_keyword_user import PixivKeywordUser

__plugin_meta__ = PluginMetadata(
    name="PIX删除",
    description="PIX关键词/UID/PID添加管理",
    usage="""
    指令：
        pix关键词 [y/n] [关键词/pid/uid]
        删除pix关键词 ['pid'/'uid'/'keyword'] [关键词/pid/uid]
        删除pix图片 *[pid]
        示例：pix关键词 y 萝莉
        示例：pix关键词 y 12312312 uid
        示例：pix关键词 n 12312312 pid
        示例：删除pix关键词 keyword 萝莉
        示例：删除pix关键词 uid 123123123
        示例：删除pix关键词 pid 123123
        示例：删除pix图片 4223442
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier", version="0.1", plugin_type=PluginType.SUPERUSER
    ).dict(),
)


_pass_matcher = on_alconna(
    Alconna(
        "pix关键词", Args["status", ["y", "n"]]["keyword", str]["type?", ["uid", "pid"]]
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

_del_matcher = on_alconna(
    Alconna("删除pix关键词", Args["type", ["pid", "uid", "keyword"]]["keyword", str]),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

_del_pic_matcher = on_alconna(
    Alconna(
        "删除pix图片",
        Args["pid", str],
        Option("-b|--black", action=store_true, help_text=""),
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)


@_pass_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    status: str,
    keyword: str,
    type: Match[str],
):
    tmp = {"group": {}, "private": {}}
    flag = status == "y"
    if type.available:
        if type.result == "uid":
            keyword = f"uid:{keyword}"
        else:
            keyword = f"pid:{keyword}"
        if not keyword[4:].isdigit():
            await MessageUtils.build_message(f"{keyword} 非全数字...").finish(
                reply_to=True
            )
    data = await PixivKeywordUser.get_or_none(keyword=keyword)
    user_id = 0
    group_id = 0
    if data:
        data.is_pass = flag
        await data.save(update_fields=["is_pass"])
        user_id, group_id = data.user_id, data.group_id
    if not user_id:
        await MessageUtils.build_message(
            f"未找到关键词/UID：{keyword}，请检查关键词/UID是否存在..."
        ).finish(reply_to=True)
    if flag:
        if group_id == -1:
            if not tmp["private"].get(user_id):
                tmp["private"][user_id] = {"keyword": [keyword]}
            else:
                tmp["private"][user_id]["keyword"].append(keyword)
        else:
            if not tmp["group"].get(group_id):
                tmp["group"][group_id] = {}
            if not tmp["group"][group_id].get(user_id):
                tmp["group"][group_id][user_id] = {"keyword": [keyword]}
            else:
                tmp["group"][group_id][user_id]["keyword"].append(keyword)
    await MessageUtils.build_message(
        f"已成功{'通过' if flag else '拒绝'}搜图关键词：{keyword}..."
    ).send()
    for user in tmp["private"]:
        text = "，".join(tmp["private"][user]["keyword"])
        await PlatformUtils.send_message(
            bot,
            user,
            None,
            f"你的关键词/UID/PID {text} 已被管理员通过，将在下一次进行更新...",
        )
        # await bot.send_private_msg(
        #     user_id=user,
        #     message=f"你的关键词/UID/PID {x} 已被管理员通过，将在下一次进行更新...",
        # )
    for group in tmp["group"]:
        for user in tmp["group"][group]:
            text = "，".join(tmp["group"][group][user]["keyword"])
            await PlatformUtils.send_message(
                bot,
                None,
                group_id=group,
                message=MessageUtils.build_message(
                    [
                        At(flag="user", target=user),
                        "你的关键词/UID/PID {x} 已被管理员通过，将在下一次进行更新...",
                    ]
                ),
            )
    logger.info(
        f" 通过了pixiv搜图关键词/UID: {keyword}", arparma.header_result, session=session
    )


@_del_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma, type: str, keyword: str):
    if type != "keyword":
        keyword = f"{type}:{keyword}"
    if data := await PixivKeywordUser.get_or_none(keyword=keyword):
        await data.delete()
        await MessageUtils.build_message(
            f"删除搜图关键词/UID：{keyword} 成功..."
        ).send()
        logger.info(
            f" 删除了pixiv搜图关键词: {keyword}", arparma.header_result, session=session
        )
    else:
        await MessageUtils.build_message(
            f"未查询到搜索关键词/UID/PID：{keyword}，删除失败！"
        ).send()


@_del_pic_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma, keyword: str):
    msg = ""
    black_pid = ""
    flag = arparma.find("black")
    img_p = None
    if "p" in keyword:
        img_p = keyword.split("p")[-1]
        keyword = keyword.replace("_", "")
        keyword = keyword[: keyword.find("p")]
    elif "ugoira" in keyword:
        img_p = keyword.split("ugoira")[-1]
        keyword = keyword.replace("_", "")
        keyword = keyword[: keyword.find("ugoira")]
    if keyword.isdigit():
        if await Pixiv.query_images(pid=int(keyword), r18=2):
            if await remove_image(int(keyword), img_p):
                msg += f'{keyword}{f"_p{img_p}" if img_p else ""}，'
                if flag:
                    if await PixivKeywordUser.exists(
                        keyword=f"black:{keyword}{f'_p{img_p}' if img_p else ''}"
                    ):
                        await PixivKeywordUser.create(
                            user_id="114514",
                            group_id="114514",
                            keyword=f"black:{keyword}{f'_p{img_p}' if img_p else ''}",
                            is_pass=False,
                        )
                        black_pid += f'{keyword}{f"_p{img_p}" if img_p else ""}，'
                logger.info(
                    f" 删除了PIX图片 PID:{keyword}{f'_p{img_p}' if img_p else ''}",
                    arparma.header_result,
                    session=session,
                )
        else:
            await MessageUtils.build_message(
                f"PIX:图片pix：{keyword}{f'_p{img_p}' if img_p else ''} 不存在...无法删除.."
            ).send()
    else:
        await MessageUtils.build_message(f"PID必须为数字！pid：{keyword}").send(
            reply_to=True
        )
    await MessageUtils.build_message(f"PIX:成功删除图片：{msg[:-1]}").send()
    if flag:
        await MessageUtils.build_message(
            f"成功图片PID加入黑名单：{black_pid[:-1]}"
        ).send()
