from typing import Tuple

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.params import Command, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me

from models.group_info import GroupInfo
from services.log import logger
from utils.depends import OneCommand
from utils.manager import requests_manager
from utils.message_builder import image
from utils.utils import is_number

__zx_plugin_name__ = "显示所有好友群组 [Superuser]"
__plugin_usage__ = """
usage：
    显示所有好友群组
    指令：
        查看所有好友/查看所有群组
        同意好友请求 [id]
        拒绝好友请求 [id]
        同意群聊请求 [id]
        拒绝群聊请求 [id]
        查看所有请求
        清空所有请求
""".strip()
__plugin_des__ = "显示所有好友群组"
__plugin_cmd__ = [
    "查看所有好友/查看所有群组",
    "同意好友请求 [id]",
    "拒绝好友请求 [id]",
    "同意群聊请求 [id]",
    "拒绝群聊请求 [id]",
    "查看所有请求",
    "清空所有请求",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


cls_group = on_command(
    "查看所有群组", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)
cls_friend = on_command(
    "查看所有好友", rule=to_me(), permission=SUPERUSER, priority=1, block=True
)

friend_handle = on_command(
    "同意好友请求", aliases={"拒绝好友请求"}, permission=SUPERUSER, priority=1, block=True
)

group_handle = on_command(
    "同意群聊请求", aliases={"拒绝群聊请求"}, permission=SUPERUSER, priority=1, block=True
)

clear_request = on_command("清空所有请求", permission=SUPERUSER, priority=1, block=True)

cls_request = on_command("查看所有请求", permission=SUPERUSER, priority=1, block=True)


@cls_group.handle()
async def _(bot: Bot):
    gl = await bot.get_group_list()
    msg = ["{group_id} {group_name}".format_map(g) for g in gl]
    msg = "\n".join(msg)
    msg = f"bot:{bot.self_id}\n| 群号 | 群名 | 共{len(gl)}个群\n" + msg
    await cls_group.send(msg)


@cls_friend.handle()
async def _(bot: Bot):
    gl = await bot.get_friend_list()
    msg = ["{user_id} {nickname}".format_map(g) for g in gl]
    msg = "\n".join(msg)
    msg = f"| QQ号 | 昵称 | 共{len(gl)}个好友\n" + msg
    await cls_friend.send(msg)


@friend_handle.handle()
async def _(bot: Bot, cmd: str = OneCommand(), arg: Message = CommandArg()):
    id_ = arg.extract_plain_text().strip()
    if is_number(id_):
        id_ = int(id_)
        if cmd[:2] == "同意":
            flag = await requests_manager.approve(bot, id_, "private")
        else:
            flag = await requests_manager.refused(bot, id_, "private")
        if flag == 1:
            await friend_handle.send(f"{cmd[:2]}好友请求失败，该请求已失效..")
            requests_manager.delete_request(id_, "private")
        elif flag == 2:
            await friend_handle.send(f"{cmd[:2]}好友请求失败，未找到此id的请求..")
        else:
            await friend_handle.send(f"{cmd[:2]}好友请求成功！")
    else:
        await friend_handle.send("id必须为纯数字！")


@group_handle.handle()
async def _(
    bot: Bot, event: MessageEvent, cmd: str = OneCommand(), arg: Message = CommandArg()
):
    id_ = arg.extract_plain_text().strip()
    flag = None
    if is_number(id_):
        id_ = int(id_)
        if cmd[:2] == "同意":
            rid = requests_manager.get_group_id(id_)
            if rid:
                if group := await GroupInfo.get_or_none(group_id=str(rid)):
                    group.group_flag = 1
                    await group.save(update_fields=["group_flag"])
                else:
                    group_info = await bot.get_group_info(group_id=rid)
                    await GroupInfo.create(
                        group_id=str(rid),
                        group_name=group_info["group_name"],
                        max_member_count=group_info["max_member_count"],
                        member_count=group_info["member_count"],
                        group_flag=1,
                    )
                flag = await requests_manager.approve(bot, id_, "group")
            else:
                await group_handle.send("同意群聊请求失败，未找到此id的请求..")
                logger.info("同意群聊请求失败，未找到此id的请求..", cmd, event.user_id)
        else:
            flag = await requests_manager.refused(bot, id_, "group")
        if flag == 1:
            await group_handle.send(f"{cmd[:2]}群聊请求失败，该请求已失效..")
            requests_manager.delete_request(id_, "group")
        elif flag == 2:
            await group_handle.send(f"{cmd[:2]}群聊请求失败，未找到此id的请求..")
        else:
            await group_handle.send(f"{cmd[:2]}群聊请求成功！")
    else:
        await group_handle.send("id必须为纯数字！")


@cls_request.handle()
async def _():
    _str = ""
    for type_ in ["private", "group"]:
        msg = await requests_manager.show(type_)
        if msg:
            _str += image(msg)
        else:
            _str += "没有任何好友请求.." if type_ == "private" else "没有任何群聊请求.."
        if type_ == "private":
            _str += "\n--------------------\n"
    await cls_request.send(Message(_str))


@clear_request.handle()
async def _():
    requests_manager.clear()
    await clear_request.send("已清空所有好友/群聊请求..")
