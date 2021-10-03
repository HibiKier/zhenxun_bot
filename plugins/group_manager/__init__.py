from nonebot import on_command, on_regex
from utils.utils import get_message_text, is_number
from nonebot.rule import to_me
from services.log import logger
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent, GROUP
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from configs.config import NICKNAME
from utils.manager import group_manager, plugins2settings_manager

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__zx_plugin_name__ = "群权限操作 [Superuser]"
__plugin_usage__ = """
usage：
    对群权限 | 群白名单 的操作
    指令：
        修改群权限 [group] [等级]
        添加群白名单 *[group]
        删除群白名单 *[group]
        查看群白名单
""".strip()
__plugin_des__ = "对群权限 | 群白名单 的操作"
__plugin_cmd__ = ["修改群权限 [group] [等级]", "添加群白名单 *[group]", "删除群白名单 *[group]", "查看群白名单"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


add_group_level = on_command("修改群权限", priority=1, permission=SUPERUSER, block=True)
my_group_level = on_command(
    "查看群权限", aliases={"群权限"}, priority=5, permission=GROUP, block=True
)
what_up_group_level = on_regex(
    ".*?(提高|提升|升高|增加|加上)(.*?)群权限.*?",
    rule=to_me(),
    priority=5,
    permission=GROUP,
    block=True,
)

manager_group_whitelist = on_command(
    "添加群白名单", aliases={"删除群白名单"}, priority=1, permission=SUPERUSER, block=True
)

show_group_whitelist = on_command(
    "查看群白名单", priority=1, permission=SUPERUSER, block=True
)


@add_group_level.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    group_id = 0
    level = 0
    if not msg:
        await add_group_level.finish("用法：修改群权限 [group] [level]")
    msg = msg.split(" ")
    if len(msg) < 2:
        await add_group_level.finish("参数不完全..[group] [level]")
    if is_number(msg[0]) and is_number(msg[1]):
        group_id = msg[0]
        level = int(msg[1])
    else:
        await add_group_level.finish("参数错误...group和level必须是数字..")
    old_level = group_manager.get_group_level(group_id)
    group_manager.set_group_level(group_id, level)
    await add_group_level.send("修改成功...", at_sender=True)
    if level > -1:
        await bot.send_group_msg(
            group_id=int(group_id), message=f"管理员修改了此群权限：{old_level} -> {level}"
        )
    logger.info(f"{event.user_id} 修改了 {group_id} 的权限：{level}")


@my_group_level.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    level = group_manager.get_group_level(event.group_id)
    tmp = ""
    data = plugins2settings_manager.get_data()
    for module in data:
        if data[module]["level"] > level:
            plugin_name = data[module]["cmd"][0]
            if plugin_name == "pixiv":
                plugin_name = "搜图 p站排行"
            tmp += f"{plugin_name}\n"
    if tmp:
        tmp = "\n目前无法使用的功能：\n" + tmp
    await my_group_level.finish(f"当前群权限：{level}{tmp}")


@what_up_group_level.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await what_up_group_level.finish(
        f"[此功能用于防止内鬼，如果引起不便那真是抱歉了]\n" f"目前提高群权限的方法：\n" f"\t1.管理员修改权限"
    )


@manager_group_whitelist.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json()).split()
    all_group = [
        g["group_id"] for g in await bot.get_group_list(self_id=int(bot.self_id))
    ]
    group_list = []
    for group in msg:
        if is_number(group) and int(group) in all_group:
            group_list.append(int(group))
    if group_list:
        for group in group_list:
            if state["_prefix"]["raw_command"] in ["添加群白名单"]:
                group_manager.add_group_white_list(group)
            else:
                group_manager.delete_group_white_list(group)
        group_list = [str(x) for x in group_list]
        await manager_group_whitelist.send(
            "已成功将 " + "\n".join(group_list) + " " + state["_prefix"]["raw_command"]
        )
    else:
        await manager_group_whitelist.send(f"添加失败，请检查{NICKNAME}是否已加入这些群聊或重复添加/删除群白单名")


@show_group_whitelist.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    x = group_manager.get_group_white_list()
    x = [str(g) for g in x]
    if x:
        await show_group_whitelist.send("目前的群白名单：\n" + "\n".join(x))
    else:
        await show_group_whitelist.send("没有任何群在群白名单...")
