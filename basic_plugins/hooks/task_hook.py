from nonebot.exception import MockApiException
from nonebot.adapters.onebot.v11 import Bot, Message
from utils.manager import group_manager
from typing import Dict, Any
import re


@Bot.on_calling_api
async def _(bot: Bot, api: str, data: Dict[str, Any]):
    r = None
    if (
        (
            (api == "send_msg" and data.get("message_type") == "group")
            or api == "send_group_msg"
        )
        and (
            (
                r := re.search(
                    "^\[\[_task\|(.*)]]",
                    data["message"].strip()
                    if isinstance(data["message"], str)
                    else str(data["message"]["text"]).strip(),
                )
            )
            or (
                r := re.search(
                    "^&#91;&#91;_task\|(.*)&#93;&#93;",
                    data["message"].strip()
                    if isinstance(data["message"], str)
                    else str(data["message"]["text"]).strip(),
                )
            )
        )
        and r.group(1) in group_manager.get_task_data().keys()
    ):
        # if bot.self_id in bot.config.superusers:
        #     raise MockApiException(f"禁止社死...")
        task = r.group(1)
        group_id = data["group_id"]
        if group_manager.get_group_level(
            group_id
        ) < 0 or not await group_manager.check_group_task_status(group_id, task):
            raise MockApiException(f"被动技能 {task} 处于关闭状态...")
        else:
            msg = str(data["message"]).strip()
            msg = msg.replace(f"&#91;&#91;_task|{task}&#93;&#93;", "").replace(
                f"[[_task|{task}]]", ""
            )
            data["message"] = Message(msg)
