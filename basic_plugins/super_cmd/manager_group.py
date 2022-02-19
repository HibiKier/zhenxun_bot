from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GROUP, GroupMessageEvent, Message
from nonebot import on_command, on_regex
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.rule import to_me
from utils.utils import is_number
from utils.manager import group_manager, plugins2settings_manager
from models.group_info import GroupInfo
from services.log import logger
from configs.config import NICKNAME
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.params import Command, CommandArg
from typing import Tuple


__zx_plugin_name__ = "管理群操作 [Superuser]"
__plugin_usage__ = """
usage：
    群权限 | 群白名单 | 退出群 操作
    指令：
        退群 [group_id]
        修改群权限 [group_id] [等级]
        添加群白名单 *[group_id]
        删除群白名单 *[group_id]
        添加群认证 *[group_id]
        删除群认证 *[group_id]
        查看群白名单
""".strip()
__plugin_des__ = "管理群操作"
__plugin_cmd__ = [
    "退群 [group_id]",
    "修改群权限 [group_id] [等级]",
    "添加群白名单 *[group_id]",
    "删除群白名单 *[group_id]",
    "添加群认证 *[group_id]",
    "删除群认证 *[group_id]",
    "查看群白名单",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


del_group = on_command("退群", rule=to_me(), permission=SUPERUSER, priority=1, block=True)

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

group_auth = on_command(
    "添加群认证", aliases={"删除群认证"}, priority=1, permission=SUPERUSER, block=True
)


@del_group.handle()
async def _(bot: Bot, arg: Message = CommandArg()):
    group_id = arg.extract_plain_text().strip()
    if group_id:
        if is_number(group_id):
            try:
                await bot.set_group_leave(group_id=int(group_id))
                logger.info(f"退出群聊 {group_id} 成功")
                await del_group.send(f"退出群聊 {group_id} 成功", at_sender=True)
                group_manager.delete_group(int(group_id))
                await GroupInfo.delete_group_info(int(group_id))
            except Exception as e:
                logger.info(f"退出群聊 {group_id} 失败 e:{e}")
        else:
            await del_group.finish(f"请输入正确的群号", at_sender=True)
    else:
        await del_group.finish(f"请输入群号", at_sender=True)


@add_group_level.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
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
async def _(event: GroupMessageEvent):
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
async def _():
    await what_up_group_level.finish(
        f"[此功能用于防止内鬼，如果引起不便那真是抱歉了]\n" f"目前提高群权限的方法：\n" f"\t1.管理员修改权限"
    )


@manager_group_whitelist.handle()
async def _(bot: Bot, cmd: Tuple[str, ...] = Command(), arg: Message = CommandArg()):
    cmd = cmd[0]
    msg = arg.extract_plain_text().strip()
    all_group = [
        g["group_id"] for g in await bot.get_group_list()
    ]
    group_list = []
    for group in msg:
        if is_number(group) and int(group) in all_group:
            group_list.append(int(group))
    if group_list:
        for group in group_list:
            if cmd in ["添加群白名单"]:
                group_manager.add_group_white_list(group)
            else:
                group_manager.delete_group_white_list(group)
        group_list = [str(x) for x in group_list]
        await manager_group_whitelist.send(
            "已成功将 " + "\n".join(group_list) + " " + cmd
        )
    else:
        await manager_group_whitelist.send(f"添加失败，请检查{NICKNAME}是否已加入这些群聊或重复添加/删除群白单名")


@show_group_whitelist.handle()
async def _():
    x = group_manager.get_group_white_list()
    x = [str(g) for g in x]
    if x:
        await show_group_whitelist.send("目前的群白名单：\n" + "\n".join(x))
    else:
        await show_group_whitelist.send("没有任何群在群白名单...")


@group_auth.handle()
async def _(bot: Bot, cmd: Tuple[str, ...] = Command(), arg: Message = CommandArg()):
    cmd = cmd[0]
    msg = arg.extract_plain_text().strip().split()
    for group_id in msg:
        if not is_number(group_id):
            await group_auth.send(f"{group_id}非纯数字，已跳过该项..")
        group_id = int(group_id)
        if cmd[:2] == "添加":
            if await GroupInfo.get_group_info(group_id):
                await GroupInfo.set_group_flag(group_id, 1)
            else:
                try:
                    group_info = await bot.get_group_info(group_id=group_id)
                except ActionFailed:
                    group_info = {
                        "group_id": group_id,
                        "group_name": "_",
                        "max_member_count": -1,
                        "member_count": -1,
                    }
                await GroupInfo.add_group_info(
                    group_info["group_id"],
                    group_info["group_name"],
                    group_info["max_member_count"],
                    group_info["member_count"],
                    1,
                )
        else:
            if await GroupInfo.get_group_info(group_id):
                await GroupInfo.set_group_flag(group_id, 0)
        await group_auth.send(
            f'已为 {group_id} {cmd[:2]}群认证..'
        )
