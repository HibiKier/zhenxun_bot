from nonebot import on_command
from .data_source import get_price, update_buff_cookie
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from utils.utils import get_message_text
from configs.config import NICKNAME


__zx_plugin_name__ = "BUFF查询皮肤"
__plugin_usage__ = """
usage：
    在线实时获取BUFF指定皮肤所有磨损底价
    指令：
        查询皮肤 [枪械名] [皮肤名称]
        示例：查询皮肤 ak47 二西莫夫
""".strip()
__plugin_des__ = "BUFF皮肤底价查询"
__plugin_cmd__ = ["查询皮肤 [枪械名] [皮肤名称]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查询皮肤"],
}


search_skin = on_command("查询皮肤", aliases={"皮肤查询"}, priority=5, block=True)


@search_skin.args_parser
async def parse(bot: Bot, event: MessageEvent, state: T_State):
    if get_message_text(event.json()) in ["取消", "算了"]:
        await search_skin.finish("已取消操作..", at_sender=True)
    state[state["_current_key"]] = str(event.get_message())


@search_skin.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.get_message()) in ["帮助"]:
        await search_skin.finish(__plugin_usage__)
    raw_arg = get_message_text(event.json())
    if _ulmt.check(event.user_id):
        await search_skin.finish("您有皮肤正在搜索，请稍等...", at_sender=True)
    if raw_arg:
        args = raw_arg.split(" ")
        if len(args) >= 2:
            state["name"] = args[0]
            state["skin"] = args[1]


@search_skin.got("name", prompt="要查询什么武器呢？")
@search_skin.got("skin", prompt="要查询该武器的什么皮肤呢？")
async def arg_handle(bot: Bot, event: MessageEvent, state: T_State):
    result = ""
    _ulmt.set_true(event.user_id)
    if state["name"] in ["ak", "ak47"]:
        state["name"] = "ak-47"
    name = state["name"] + " | " + state["skin"]
    try:
        result, status_code = await get_price(name)
    except FileNotFoundError:
        await search_skin.finish(f'请先对{NICKNAME}说"设置cookie"来设置cookie！')
    if status_code in [996, 997, 998]:
        _ulmt.set_false(event.user_id)
        await search_skin.finish(result)
    if result:
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 查询皮肤:"
            + name
        )
        _ulmt.set_false(event.user_id)
        await search_skin.finish(result)
    else:
        logger.info(
            f"USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}"
            f" 查询皮肤：{name} 没有查询到"
        )
        _ulmt.set_false(event.user_id)
        await search_skin.finish("没有查询到哦，请检查格式吧")


update_buff_session = on_command(
    "更新cookie", aliases={"设置cookie"}, rule=to_me(), permission=SUPERUSER, priority=1
)


@update_buff_session.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_buff_session.finish(
        update_buff_cookie(str(event.get_message())), at_sender=True
    )
