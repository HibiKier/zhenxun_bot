from typing import Tuple

from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import (
    GROUP,
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
)
from nonebot.params import Command, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me

from configs.config import NICKNAME
from models.group_info import GroupInfo
from services.log import logger
from utils.depends import OneCommand
from utils.image_utils import text2image
from utils.manager import group_manager, plugins2settings_manager
from utils.message_builder import image
from utils.utils import is_number

__zx_plugin_name__ = "管理群操作 [Superuser]"
__plugin_usage__ = """
usage：
    群权限 | 群白名单 | 退出群 操作
    退群，添加/删除群白名单，添加/删除群认证，当在群聊中这五个命令且没有指定群号时，默认指定当前群聊
    指令:
        退群 ?[group_id]
        修改群权限 [group_id] [等级]
        修改群权限 [等级]: 该命令仅在群聊时生效，默认修改当前群聊
        添加群白名单 ?*[group_id]
        删除群白名单 ?*[group_id]
        添加群认证 ?*[group_id]
        删除群认证 ?*[group_id]
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
    "(:?提高|提升|升高|增加|加上).*?群权限",
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
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    group_id = arg.extract_plain_text().strip()
    if not group_id and isinstance(event, GroupMessageEvent):
        group_id = event.group_id
    if group_id:
        if is_number(group_id):
            group_list = [x["group_id"] for x in await bot.get_group_list()]
            group_id = int(group_id)
            if group_id not in group_list:
                logger.debug("群聊不存在", "退群", event.user_id, target=group_id)
                await del_group.finish(f"{NICKNAME}未在该群聊中...")
            try:
                await bot.set_group_leave(group_id=group_id)
                logger.info(f"{NICKNAME}退出群聊成功", "退群", event.user_id, target=group_id)
                await del_group.send(f"退出群聊 {group_id} 成功", at_sender=True)
                group_manager.delete_group(group_id)
                await GroupInfo.filter(group_id=group_id).delete()
            except Exception as e:
                logger.error(f"退出群聊失败", "退群", event.user_id, target=group_id, e=e)
                await del_group.send(f"退出群聊 {group_id} 失败", at_sender=True)
        else:
            await del_group.send(f"请输入正确的群号", at_sender=True)
    else:
        await del_group.send(f"请输入群号", at_sender=True)


@add_group_level.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    msg = msg.split()
    group_id = 0
    level = 0
    if isinstance(event, GroupMessageEvent) and len(msg) == 1:
        msg = [event.group_id, msg[0]]
    if not msg:
        await add_group_level.finish("缺失参数...")
    if len(msg) < 2:
        await add_group_level.finish("缺失参数...")
    if is_number(msg[0]) and is_number(msg[1]):
        group_id = str(msg[0])
        level = int(msg[1])
    else:
        await add_group_level.finish("参数错误...群号和等级必须是数字..")
    old_level = group_manager.get_group_level(group_id)
    group_manager.set_group_level(group_id, level)
    await add_group_level.send("修改成功...", at_sender=True)
    if level > -1:
        await bot.send_group_msg(
            group_id=int(group_id), message=f"管理员修改了此群权限：{old_level} -> {level}"
        )
    logger.info(f"修改群权限：{level}", "修改群权限", event.user_id, target=group_id)


@my_group_level.handle()
async def _(event: GroupMessageEvent):
    level = group_manager.get_group_level(event.group_id)
    tmp = ""
    data = plugins2settings_manager.get_data()
    for module in data:
        if data[module].level > level:
            plugin_name = data[module].cmd[0]
            if plugin_name == "pixiv":
                plugin_name = "搜图 p站排行"
            tmp += f"{plugin_name}\n"
    if not tmp:
        await my_group_level.finish(f"当前群权限：{level}")
    await my_group_level.finish(
        f"当前群权限：{level}\n目前无法使用的功能:\n"
        + image(await text2image(tmp, padding=10, color="#f9f6f2"))
    )


@what_up_group_level.handle()
async def _():
    await what_up_group_level.finish(
        f"[此功能用于防止内鬼，如果引起不便那真是抱歉了]\n" f"目前提高群权限的方法：\n" f"\t1.超级管理员修改权限"
    )


@manager_group_whitelist.handle()
async def _(
    bot: Bot, event: MessageEvent, cmd: str = OneCommand(), arg: Message = CommandArg()
):
    msg = arg.extract_plain_text().strip().split()
    if not msg and isinstance(event, GroupMessageEvent):
        msg = [event.group_id]
    if not msg:
        await manager_group_whitelist.finish("请输入群号")
    all_group = [g["group_id"] for g in await bot.get_group_list()]
    error_group = []
    group_list = []
    for group_id in msg:
        if is_number(group_id) and int(group_id) in all_group:
            group_list.append(int(group_id))
        else:
            logger.debug(f"群号不合法或不存在", cmd, target=group_id)
            error_group.append(group_id)
    if group_list:
        for group_id in group_list:
            if cmd in ["添加群白名单"]:
                group_manager.add_group_white_list(group_id)
            else:
                group_manager.delete_group_white_list(group_id)
        group_list = [str(x) for x in group_list]
        await manager_group_whitelist.send("已成功将 " + "\n".join(group_list) + " " + cmd)
        group_manager.save()
    if error_group:
        await manager_group_whitelist.send("以下群聊不合法或不存在:\n" + "\n".join(error_group))


@show_group_whitelist.handle()
async def _():
    group = [str(g) for g in group_manager.get_group_white_list()]
    if not group:
        await show_group_whitelist.finish("没有任何群在群白名单...")
    await show_group_whitelist.send("目前的群白名单:\n" + "\n".join(group))


@group_auth.handle()
async def _(
    bot: Bot, event: MessageEvent, cmd: str = OneCommand(), arg: Message = CommandArg()
):
    msg = arg.extract_plain_text().strip().split()
    if isinstance(event, GroupMessageEvent) and not msg:
        msg = [event.group_id]
    if not msg:
        await manager_group_whitelist.finish("请输入群号")
    error_group = []
    for group_id in msg:
        group_id = int(group_id)
        if cmd[:2] == "添加":
            try:
                await GroupInfo.update_or_create(
                    group_id=group_id,
                    defaults={
                        "group_flag": 1,
                    },
                )
            except Exception as e:
                await group_auth.send(f"添加群认证 {group_id} 发生错误！")
                logger.error(f"添加群认证发生错误", cmd, target=group_id, e=e)
            else:
                await group_auth.send(f"已为 {group_id} {cmd[:2]}群认证..")
                logger.info(f"添加群认证成功", cmd, target=group_id)
        else:
            if group := await GroupInfo.filter(group_id=group_id).first():
                await group.update_or_create(
                    group_id=group_id, defaults={"group_flag": 0}
                )
                await group_auth.send(f"已删除 {group_id} 群认证..")
                logger.info(f"删除群认证成功", cmd, target=group_id)
            else:
                await group_auth.send(f"未查找到群聊: {group_id}")
                logger.info(f"未找到群聊", cmd, target=group_id)
    if error_group:
        await manager_group_whitelist.send("以下群聊不合法或不存在:\n" + "\n".join(error_group))
