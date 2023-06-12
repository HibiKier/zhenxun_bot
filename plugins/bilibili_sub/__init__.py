from typing import Any, Optional, Tuple

import nonebot
from nonebot import Driver, on_command, on_regex
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.params import ArgStr, CommandArg, RegexGroup
from nonebot.typing import T_State

from configs.config import Config
from models.level_user import LevelUser
from services.log import logger
from utils.depends import GetConfig
from utils.image_utils import text2image
from utils.manager import group_manager
from utils.message_builder import image
from utils.utils import get_bot, is_number, scheduler

from .data_source import (
    BilibiliSub,
    SubManager,
    add_live_sub,
    add_season_sub,
    add_up_sub,
    delete_sub,
    get_media_id,
    get_sub_status,
)

__zx_plugin_name__ = "B站订阅"
__plugin_usage__ = """
usage：
    B站直播，番剧，UP动态开播等提醒
    主播订阅相当于 直播间订阅 + UP订阅
    指令：[示例Id乱打的，仅做示例]
        添加订阅 ['主播'/'UP'/'番剧'] [id/链接/番名]
        删除订阅 ['主播'/'UP'/'id'] [id]
        查看订阅
        示例：添加订阅主播 2345344 <-(直播房间id)
        示例：添加订阅UP 2355543 <-(个人主页id)
        示例：添加订阅番剧 史莱姆 <-(支持模糊搜索)
        示例：添加订阅番剧 125344 <-(番剧id)
        示例：删除订阅id 2324344 <-(任意id，通过查看订阅获取)
""".strip()
__plugin_des__ = "非常便利的B站订阅通知"
__plugin_cmd__ = ["添加订阅 [主播/UP/番剧] [id/链接/番名]", "删除订阅 ['主播'/'UP'/'id'] [id]", "查看订阅"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier & NumberSir"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["B站订阅", "b站订阅", "添加订阅", "删除订阅", "查看订阅"],
}
__plugin_configs__ = {
    "GROUP_BILIBILI_SUB_LEVEL": {
        "value": 5,
        "help": "群内bilibili订阅需要管理的权限",
        "default_value": 5,
        "type": int,
    },
    "LIVE_MSG_AT_ALL": {
        "value": False,
        "help": "直播提醒是否AT全体（仅在真寻是管理员时生效）",
        "default_value": False,
        "type": bool,
    },
    "UP_MSG_AT_ALL": {
        "value": False,
        "help": "UP动态投稿提醒是否AT全体（仅在真寻是管理员时生效）",
        "default_value": False,
        "type": bool,
    },
}

add_sub = on_command("添加订阅", priority=5, block=True)
del_sub = on_command("删除订阅", priority=5, block=True)
show_sub_info = on_regex("^查看订阅$", priority=5, block=True)

driver: Driver = nonebot.get_driver()


sub_manager: SubManager


@driver.on_startup
async def _():
    global sub_manager
    sub_manager = SubManager()


@add_sub.handle()
@del_sub.handle()
async def _(
    event: MessageEvent,
    state: T_State,
    arg: Message = CommandArg(),
    sub_level: Optional[int] = GetConfig(config="GROUP_BILIBILI_SUB_LEVEL"),
):
    msg = arg.extract_plain_text().strip().split()
    if len(msg) < 2:
        await add_sub.finish("参数不完全，请查看订阅帮助...")
    sub_type = msg[0]
    id_ = ""
    if isinstance(event, GroupMessageEvent):
        if not await LevelUser.check_level(
            event.user_id,
            event.group_id,
            sub_level,  # type: ignore
        ):
            await add_sub.finish(
                f"您的权限不足，群内订阅的需要 {sub_level} 级权限..",
                at_sender=True,
            )
        sub_user = f"{event.user_id}:{event.group_id}"
    else:
        sub_user = f"{event.user_id}"
    state["sub_type"] = sub_type
    state["sub_user"] = sub_user
    if len(msg) > 1:
        if "http" in msg[1]:
            msg[1] = msg[1].split("?")[0]
            msg[1] = msg[1][:-1] if msg[1][-1] == "/" else msg[1]
            msg[1] = msg[1].split("/")[-1]
        id_ = msg[1][2:] if msg[1].startswith("md") else msg[1]
    if not is_number(id_):
        if sub_type in ["season", "动漫", "番剧"]:
            rst = "*以为您找到以下番剧，请输入Id选择：*\n"
            state["season_data"] = await get_media_id(id_)
            if len(state["season_data"]) == 0:  # type: ignore
                await add_sub.finish(f"未找到番剧：{msg}")
            for i, x in enumerate(state["season_data"]):  # type: ignore
                rst += f'{i + 1}.{state["season_data"][x]["title"]}\n----------\n'  # type: ignore
            await add_sub.send("\n".join(rst.split("\n")[:-1]))
        else:
            await add_sub.finish("Id 必须为全数字！")
    else:
        state["id"] = int(id_)


@add_sub.got("sub_type")
@add_sub.got("sub_user")
@add_sub.got("id")
async def _(
    event: MessageEvent,
    state: T_State,
    id_: str = ArgStr("id"),
    sub_type: str = ArgStr("sub_type"),
    sub_user: str = ArgStr("sub_user"),
):
    if sub_type in ["season", "动漫", "番剧"] and state.get("season_data"):
        season_data = state["season_data"]
        if not is_number(id_) or int(id_) < 1 or int(id_) > len(season_data):
            await add_sub.reject_arg("id", "Id必须为数字且在范围内！请重新输入...")
        id_ = season_data[int(id_) - 1]["media_id"]
    if sub_type in ["主播", "直播"]:
        await add_sub.send(await add_live_sub(id_, sub_user))
    elif sub_type.lower() in ["up", "用户"]:
        await add_sub.send(await add_up_sub(id_, sub_user))
    elif sub_type in ["season", "动漫", "番剧"]:
        await add_sub.send(await add_season_sub(id_, sub_user))
    else:
        await add_sub.finish("参数错误，第一参数必须为：主播/up/番剧！")
    logger.info(
        f"添加订阅：{sub_type} -> {sub_user} -> {id_}",
        "添加订阅",
        event.user_id,
        getattr(event, "group_id", None),
    )


@del_sub.got("sub_type")
@del_sub.got("sub_user")
@del_sub.got("id")
async def _(
    event: MessageEvent,
    id_: str = ArgStr("id"),
    sub_type: str = ArgStr("sub_type"),
    sub_user: str = ArgStr("sub_user"),
):
    if sub_type in ["主播", "直播"]:
        result = await BilibiliSub.delete_bilibili_sub(id_, sub_user, "live")
    elif sub_type.lower() in ["up", "用户"]:
        result = await BilibiliSub.delete_bilibili_sub(id_, sub_user, "up")
    else:
        result = await BilibiliSub.delete_bilibili_sub(id_, sub_user)
    if result:
        await del_sub.send(f"删除订阅id：{id_} 成功...")
        logger.info(
            f"删除订阅 {id_}",
            "删除订阅",
            event.user_id,
            getattr(event, "group_id", None),
        )
    else:
        await del_sub.send(f"删除订阅id：{id_} 失败...")
        logger.info(
            f"删除订阅 {id_} 失败",
            "删除订阅",
            event.user_id,
            getattr(event, "group_id", None),
        )


@show_sub_info.handle()
async def _(event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        id_ = f"{event.group_id}"
    else:
        id_ = f"{event.user_id}"
    data = await BilibiliSub.filter(sub_users__contains=id_).all()
    live_rst = ""
    up_rst = ""
    season_rst = ""
    for x in data:
        if x.sub_type == "live":
            live_rst += (
                f"\t直播间id：{x.sub_id}\n" f"\t名称：{x.uname}\n" f"------------------\n"
            )
        if x.sub_type == "up":
            up_rst += f"\tUP：{x.uname}\n" f"\tuid：{x.uid}\n" f"------------------\n"
        if x.sub_type == "season":
            season_rst += (
                f"\t番剧id：{x.sub_id}\n"
                f"\t番名：{x.season_name}\n"
                f"\t当前集数：{x.season_current_episode}\n"
                f"------------------\n"
            )
    live_rst = "当前订阅的直播：\n" + live_rst if live_rst else live_rst
    up_rst = "当前订阅的UP：\n" + up_rst if up_rst else up_rst
    season_rst = "当前订阅的番剧：\n" + season_rst if season_rst else season_rst
    if not live_rst and not up_rst and not season_rst:
        live_rst = (
            "该群目前没有任何订阅..." if isinstance(event, GroupMessageEvent) else "您目前没有任何订阅..."
        )
    await show_sub_info.send(
        image(
            await text2image(
                live_rst + up_rst + season_rst, padding=10, color="#f9f6f2"
            )
        )
    )


# 推送
@scheduler.scheduled_job(
    "interval",
    seconds=30,
)
async def _():
    bot = get_bot()
    sub = None
    if bot:
        await sub_manager.reload_sub_data()
        sub = await sub_manager.random_sub_data()
        if sub:
            try:
                logger.debug(f"Bilibili订阅开始检测：{sub.sub_id}")
                rst = await get_sub_status(sub.sub_id, sub.sub_type)
                await send_sub_msg(rst or "", sub, bot)  # type: ignore
                if sub.sub_type == "live":
                    rst = await get_sub_status(sub.sub_id, "up")
                    await send_sub_msg(rst or "", sub, bot)  # type: ignore
            except Exception as e:
                logger.error(f"B站订阅推送发生错误 sub_id：{sub.sub_id}", e=e)


async def send_sub_msg(rst: str, sub: BilibiliSub, bot: Bot):
    """
    推送信息
    :param rst: 回复
    :param sub: BilibiliSub
    :param bot: Bot
    """
    temp_group = []
    if rst:
        for x in sub.sub_users.split(",")[:-1]:
            try:
                if ":" in x and x.split(":")[1] not in temp_group:
                    group_id = int(x.split(":")[1])
                    temp_group.append(group_id)
                    if (
                        await bot.get_group_member_info(
                            group_id=group_id, user_id=int(bot.self_id), no_cache=True
                        )
                    )["role"] in ["owner", "admin"]:
                        if (
                            sub.sub_type == "live"
                            and Config.get_config("bilibili_sub", "LIVE_MSG_AT_ALL")
                        ) or (
                            sub.sub_type == "up"
                            and Config.get_config("bilibili_sub", "UP_MSG_AT_ALL")
                        ):
                            rst = "[CQ:at,qq=all]\n" + rst
                    if group_manager.get_plugin_status("bilibili_sub", group_id):
                        await bot.send_group_msg(
                            group_id=group_id, message=Message(rst)
                        )
                else:
                    await bot.send_private_msg(user_id=int(x), message=Message(rst))
            except Exception as e:
                logger.error(f"B站订阅推送发生错误 sub_id：{sub.sub_id}", e=e)
