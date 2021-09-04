from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent, Message
from .data_source import (
    add_live_sub,
    delete_sub,
    add_up_sub,
    add_season_sub,
    get_media_id,
    get_sub_status,
    SubManager,
)
from models.level_user import LevelUser
from configs.config import GROUP_BILIBILI_SUB_LEVEL
from utils.utils import get_message_text, is_number, scheduler, get_bot
from models.bilibili_sub import BilibiliSub
from typing import Optional
from services.log import logger
from nonebot import Driver
import nonebot

__plugin_name__ = "B站订阅"

__plugin_usage__ = """B站订阅帮助：
    添加订阅 [主播/UP/番剧] [id/链接/番名]
    删除订阅 [id]
    查看订阅"""

add_sub = on_command("添加订阅", priority=5, block=True)
del_sub = on_command("删除订阅", priority=5, block=True)
show_sub_info = on_command('查看订阅', priority=5, block=True)

driver: Driver = nonebot.get_driver()


sub_manager: Optional[SubManager] = None


@driver.on_startup
async def _():
    global sub_manager
    sub_manager = SubManager()


@add_sub.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    season_data = state["season_data"]
    msg = get_message_text(event.json())
    if not is_number(msg) or int(msg) < 1 or int(msg) > len(season_data):
        await add_sub.reject("Id必须为数字且在范围内！请重新输入...")
    state["id"] = season_data[int(msg) - 1]["media_id"]


@add_sub.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json()).split()
    if len(msg) < 2:
        await add_sub.finish("参数不完全，请查看订阅帮助...")
    sub_type = msg[0]
    id_ = ""
    if isinstance(event, GroupMessageEvent):
        if not await LevelUser.check_level(
            event.user_id, event.group_id, GROUP_BILIBILI_SUB_LEVEL
        ):
            await add_sub.finish(
                f"您的权限不足，群内订阅的需要 {GROUP_BILIBILI_SUB_LEVEL} 级权限..", at_sender=True
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
            print(state["season_data"])
            if len(state["season_data"]) == 0:
                await add_sub.finish(f"未找到番剧：{msg}")
            for i, x in enumerate(state["season_data"]):
                rst += f'{i + 1}.{state["season_data"][x]["title"]}\n----------\n'
            await add_sub.send("\n".join(rst.split("\n")[:-1]))
        else:
            await add_sub.finish("Id 必须为全数字！")
    else:
        state["id"] = int(id_)


@add_sub.got("id")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    sub_type = state["sub_type"]
    sub_user = state["sub_user"]
    id_ = state["id"]
    if sub_type in ["主播", "直播"]:
        await add_sub.send(await add_live_sub(id_, sub_user))
    elif sub_type.lower() in ["up", "用户"]:
        await add_sub.send(await add_up_sub(id_, sub_user))
    elif sub_type in ["season", "动漫", "番剧"]:
        await add_sub.send(await add_season_sub(id_, sub_user))
    else:
        await add_sub.finish("参数错误，第一参数必须为：主播/up/番剧！")
    sub_manager.reload_flag = True
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 添加订阅：{sub_type} -> {sub_user} -> {id_}"
    )


@del_sub.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not is_number(msg):
        await del_sub.finish('Id必须为数字！', at_sender=True)
    id_ = f'{event.user_id}:{event.group_id}' if isinstance(event, GroupMessageEvent) else f'{event.user_id}'
    if await BilibiliSub.delete_bilibili_sub(int(msg), id_):
        await del_sub.send(f'删除订阅id：{msg} 成功...')
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 删除订阅 {id_}"
        )
    else:
        await del_sub.send(f'删除订阅id：{msg} 失败...')


@show_sub_info.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    id_ = f'{event.user_id}:{event.group_id}' if isinstance(event, GroupMessageEvent) else f'{event.user_id}'
    data = await BilibiliSub.get_sub_data(id_)
    live_rst = ''
    up_rst = ''
    season_rst = ''
    for x in data:
        if x.sub_type == 'live':
            live_rst += f'\t直播间id：{x.sub_id}\n' \
                        f'\t名称：{x.uname}\n' \
                        f'------------------\n'
        if x.sub_type == 'up':
            up_rst += f'\tUP：{x.uname}\n' \
                      f'\tuid：{x.uid}\n' \
                      f'------------------\n'
        if x.sub_type == 'season':
            season_rst += f'\t番名：{x.season_name}\n' \
                          f'\t当前集数：{x.season_current_episode}\n' \
                          f'------------------\n'
    live_rst = '当前订阅的直播：\n' + live_rst if live_rst else live_rst
    up_rst = '当前订阅的UP：\n' if up_rst else up_rst
    season_rst = '当前订阅的番剧：\n' if season_rst else season_rst
    if not live_rst and not up_rst and not season_rst:
        live_rst = '您目前没有任何订阅...'
    await show_sub_info.send(live_rst + up_rst + season_rst)


# 推送
@scheduler.scheduled_job(
    "interval",
    seconds=30,
)
async def _():
    bot = get_bot()
    sub = None
    if bot:
        try:
            await sub_manager.reload_sub_data()
            sub = await sub_manager.random_sub_data()
            if sub:
                rst = await get_sub_status(sub.sub_id, sub.sub_type)
                await send_sub_msg(rst, sub, bot)
                if sub.sub_type == "live":
                    rst = await get_sub_status(sub.sub_id, "up")
                    await send_sub_msg(rst, sub, bot)
        except Exception as e:
            logger.error(f"B站订阅推送发生错误 sub_id：{sub.sub_id if sub else 0} {type(e)}：{e}")


async def send_sub_msg(rst: str, sub: BilibiliSub, bot: Bot):
    """
    推送信息
    :param rst: 回复
    :param sub: BilibiliSub
    :param bot: Bot
    """
    if rst:
        for x in sub.sub_users.split(",")[:-1]:
            try:
                if ":" in x:
                    await bot.send_group_msg(
                        group_id=int(x.split(":")[1]), message=Message(rst)
                    )
                else:
                    await bot.send_private_msg(user_id=int(x), message=Message(rst))
            except Exception as e:
                logger.error(f"B站订阅推送发生错误 sub_id：{sub.sub_id} {type(e)}：{e}")
