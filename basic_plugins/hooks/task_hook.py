import re
from typing import Any, Dict

from nonebot.adapters.onebot.v11 import Bot, Message, unescape
from nonebot.exception import MockApiException

from services.log import logger
from utils.manager import group_manager


@Bot.on_calling_api
async def _(bot: Bot, api: str, data: Dict[str, Any]):
    r = None
    task = None
    group_id = None
    try:
        if (
            api == "send_msg" and data.get("message_type") == "group"
        ) or api == "send_group_msg":
            msg = unescape(
                data["message"].strip()
                if isinstance(data["message"], str)
                else str(data["message"]["text"]).strip()
            )
            if r := re.search(
                "^\[\[_task\|(.*)]]",
                msg,
            ):
                if r.group(1) in group_manager.get_task_data().keys():
                    task = r.group(1)
                    group_id = data["group_id"]
    except Exception as e:
        logger.error(f"TaskHook ERROR", "HOOK", e=e)
    else:
        if task and group_id:
            if group_manager.get_group_level(
                group_id
            ) < 0 or not group_manager.check_task_status(task, group_id):
                logger.debug(f"被动技能 {task} 处于关闭状态")
                raise MockApiException(f"被动技能 {task} 处于关闭状态...")
            else:
                msg = str(data["message"]).strip()
                msg = msg.replace(f"&#91;&#91;_task|{task}&#93;&#93;", "").replace(
                    f"[[_task|{task}]]", ""
                )
                data["message"] = Message(msg)
