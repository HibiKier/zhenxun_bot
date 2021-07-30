from typing import Any, Dict
from nonebot import get_driver, on_command
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent, PrivateMessageEvent
from nonebot.rule import to_me
from nonebot.typing import T_State, T_CalledAPIHook

from .config import Config

global_config = get_driver().config
withdraw_config = Config(**global_config.dict())

msg_ids = {}
max_size = withdraw_config.withdraw_max_size


__plugin_name__ = "撤回"

__plugin_usage__ = (
    "用法：撤回 [消息位置](默认0)\n" "示例：\n" "\t撤回0  -> 撤回倒数第一条消息(即最新发送的消息)" "\t撤回1  -> 撤回倒数第2条消息"
)


def get_key(msg_type, id):
    return f"{msg_type}_{id}"


async def save_msg_id(
    bot: Bot, e: Exception, api: str, data: Dict[str, Any], result: Any
) -> T_CalledAPIHook:
    try:
        if api == "send_msg":
            msg_type = data["message_type"]
            id = data["group_id"] if msg_type == "group" else data["user_id"]
        elif api == "send_private_msg":
            msg_type = "private"
            id = data["user_id"]
        elif api == "send_group_msg":
            msg_type = "group"
            id = data["group_id"]
        else:
            return
        key = get_key(msg_type, id)
        msg_id = result["message_id"]

        if key not in msg_ids:
            msg_ids[key] = []
        msg_ids[key].append(msg_id)
        if len(msg_ids) > max_size:
            msg_ids[key].pop(0)
    except:
        pass


Bot._called_api_hook.add(save_msg_id)


withdraw = on_command("withdraw", aliases={"撤回"}, rule=to_me(), priority=1, block=True)


@withdraw.handle()
async def _(bot: Bot, event: Event, state: T_State):
    if isinstance(event, GroupMessageEvent):
        msg_type = "group"
        id = event.group_id
    elif isinstance(event, PrivateMessageEvent):
        msg_type = "private"
        id = event.user_id
    else:
        return
    key = get_key(msg_type, id)

    num = event.get_plaintext().strip()
    if not num:
        num = 0
    elif num.isdigit() and 0 <= int(num) < len(msg_ids[key]):
        num = int(num)
    else:
        return

    try:
        idx = -num - 1
        await bot.delete_msg(message_id=msg_ids[key][idx])
        msg_ids[key].pop(idx)
    except:
        await withdraw.finish("撤回失败，可能已超时")
