from nonebot import on_command
from .data_source import get_price, update_buff_cookie
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg, ArgStr
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
__plugin_block_limit__ = {"rst": "您有皮肤正在搜索，请稍等..."}
__plugin_configs__ = {
    "BUFF_PROXY": {"value": None, "help": "BUFF代理，有些厂ip可能被屏蔽"},
    "COOKIE": {"value": None, "help": "BUFF的账号cookie"},
}


search_skin = on_command("查询皮肤", aliases={"皮肤查询"}, priority=5, block=True)


@search_skin.handle()
async def _(event: MessageEvent, state: T_State, arg: Message = CommandArg()):
    raw_arg = arg.extract_plain_text().strip()
    if raw_arg:
        args = raw_arg.split()
        if len(args) >= 2:
            state["name"] = args[0]
            state["skin"] = args[1]


@search_skin.got("name", prompt="要查询什么武器呢？")
@search_skin.got("skin", prompt="要查询该武器的什么皮肤呢？")
async def arg_handle(
    event: MessageEvent,
    state: T_State,
    name: str = ArgStr("name"),
    skin: str = ArgStr("skin"),
):
    if name in ["算了", "取消"] or skin in ["算了", "取消"]:
        await search_skin.finish("已取消操作...")
    result = ""
    if name in ["ak", "ak47"]:
        name = "ak-47"
    name = name + " | " + skin
    try:
        result, status_code = await get_price(name)
    except FileNotFoundError:
        await search_skin.finish(f'请先对{NICKNAME}说"设置cookie"来设置cookie！')
    if status_code in [996, 997, 998]:
        await search_skin.finish(result)
    if result:
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 查询皮肤:"
            + name
        )
        await search_skin.finish(result)
    else:
        logger.info(
            f"USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}"
            f" 查询皮肤：{name} 没有查询到"
        )
        await search_skin.finish("没有查询到哦，请检查格式吧")


update_buff_session = on_command(
    "更新cookie", aliases={"设置cookie"}, rule=to_me(), permission=SUPERUSER, priority=1
)


@update_buff_session.handle()
async def _(event: MessageEvent):
    await update_buff_session.finish(
        update_buff_cookie(str(event.get_message())), at_sender=True
    )
