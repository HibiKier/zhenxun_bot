from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message
from nonebot.rule import to_me
from utils.utils import get_message_text, is_number
from utils.manager import requests_manager
from utils.message_builder import image
from models.group_info import GroupInfo


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
async def _(bot: Bot, event: MessageEvent, state: T_State):
    gl = await bot.get_group_list(self_id=int(bot.self_id))
    msg = ["{group_id} {group_name}".format_map(g) for g in gl]
    msg = "\n".join(msg)
    msg = f"bot:{bot.self_id}\n| 群号 | 群名 | 共{len(gl)}个群\n" + msg
    await bot.send_private_msg(
        self_id=int(bot.self_id),
        user_id=int(list(bot.config.superusers)[0]),
        message=msg,
    )


@cls_friend.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    gl = await bot.get_friend_list(self_id=int(bot.self_id))
    msg = ["{user_id} {nickname}".format_map(g) for g in gl]
    msg = "\n".join(msg)
    msg = f"| QQ号 | 昵称 | 共{len(gl)}个好友\n" + msg
    await bot.send_private_msg(
        self_id=int(bot.self_id),
        user_id=int(list(bot.config.superusers)[0]),
        message=msg,
    )


@friend_handle.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    id_ = get_message_text(event.json())
    if is_number(id_):
        id_ = int(id_)
        if state["_prefix"]["raw_command"][:2] == "同意":
            if await requests_manager.approve(bot, id_, "private"):
                await friend_handle.send("同意好友请求成功..")
            else:
                await friend_handle.send("同意好友请求失败，可能是未找到此id的请求..")
        else:
            if await requests_manager.refused(bot, id_, "private"):
                await friend_handle.send("拒绝好友请求成功..")
            else:
                await friend_handle.send("拒绝好友请求失败，可能是未找到此id的请求..")
    else:
        await friend_handle.send("id必须为纯数字！")


@group_handle.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    id_ = get_message_text(event.json())
    if is_number(id_):
        id_ = int(id_)
        if state["_prefix"]["raw_command"][:2] == "同意":
            rid = await requests_manager.approve(bot, id_, "group")
            if rid:
                await friend_handle.send("同意群聊请求成功..")
                if await GroupInfo.get_group_info(rid):
                    await GroupInfo.set_group_flag(rid, 1)
                else:
                    group_info = await bot.get_group_info(group_id=rid)
                    await GroupInfo.add_group_info(
                        rid,
                        group_info["group_name"],
                        group_info["max_member_count"],
                        group_info["member_count"],
                        1
                    )
            else:
                await friend_handle.send("同意群聊请求失败，可能是未找到此id的请求..")
        else:
            if await requests_manager.refused(bot, id_, "group"):
                await friend_handle.send("拒绝群聊请求成功..")
            else:
                await friend_handle.send("拒绝群聊请求失败，可能是未找到此id的请求..")
    else:
        await friend_handle.send("id必须为纯数字！")


@cls_request.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    _str = ""
    for type_ in ["private", "group"]:
        msg = await requests_manager.show(type_)
        if msg:
            _str += image(b64=msg)
        else:
            _str += "没有任何好友请求.." if type_ == "private" else "没有任何群聊请求.."
        if type_ == "private":
            _str += '\n--------------------\n'
    await cls_request.send(Message(_str))


@clear_request.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    requests_manager.clear()
    await cls_request.send("已清空所有好友/群聊请求..")
