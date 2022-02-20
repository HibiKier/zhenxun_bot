from nonebot.exception import MockApiException
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from utils.manager import group_manager
from utils.utils import get_message_text
from typing import Dict, Any
import re


@Bot.on_calling_api
async def handle_api_call(bot: Bot, api: str, data: Dict[str, Any]):
    r = None
    if (
        (api == "send_msg" and data["message"] == "group_id" or api == "send_group_msg")
        and (
            r := re.search(
                "^\[\[_task\|(.*)]]",
                data["message"]
                if isinstance(data["message"], str)
                else get_message_text(data["message"]),
            )
        )
        and r.group(1) in group_manager.get_task_data().keys()
    ):
        task = r.group(1)
        group_id = data["group_id"]
        if not await group_manager.check_group_task_status(group_id, task):
            raise MockApiException(f"被动技能 {task} 处于关闭状态...")
        else:
            if isinstance(data["message"], str):
                msg = data["message"]
                msg = msg.replace(f"[[_task|{task}]]", "")
                data["message"] = msg
            else:
                msg = str(data["message"][0])
                msg = msg.replace(f"&#91;&#91;_task|{task}&#93;&#93;", "")
                data["message"][0] = MessageSegment.text(msg)
