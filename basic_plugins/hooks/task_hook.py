from nonebot.exception import MockApiException
from nonebot.adapters.onebot.v11 import Bot, Message
from utils.manager import group_manager
from services.log import logger
from typing import Dict, Any
import re


@Bot.on_calling_api
async def _(bot: Bot, api: str, data: Dict[str, Any]):
    r = None
    task = None
    group_id = None
    try:
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
            task = r.group(1)
            group_id = data["group_id"]
    except Exception as e:
        logger.error(f"TaskHook ERROR {type(e)}：{e}")
    else:
        if task and group_id:
            if (
                group_manager.get_group_level(group_id) < 0
                or not group_manager.check_task_status(task, group_id)
            ):
                raise MockApiException(f"被动技能 {task} 处于关闭状态...")
            else:
                msg = str(data["message"]).strip()
                msg = msg.replace(f"&#91;&#91;_task|{task}&#93;&#93;", "").replace(
                    f"[[_task|{task}]]", ""
                )
                data["message"] = Message(msg)
