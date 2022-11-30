from pydantic.error_wrappers import ValidationError
from services.log import logger
from utils.manager import group_manager
from utils.utils import get_bot

from ..auth import Depends, User, token_to_user
from ..config import *


@app.get("/webui/group")
async def _(user: User = Depends(token_to_user)) -> Result:
    """
    获取群信息
    """
    group_list_result = []
    group_info = {}
    if bot := get_bot():
        group_list = await bot.get_group_list()
        for g in group_list:
            group_info[g["group_id"]] = Group(**g)
    group_data = group_manager.get_data()
    for group_id in group_data.group_manager:
        try:
            task_list = []
            data = group_manager[group_id].dict()
            for tn, status in data["group_task_status"].items():
                task_list.append(
                    Task(
                        **{
                            "name": tn,
                            "nameZh": group_manager.get_task_data().get(tn) or tn,
                            "status": status,
                        }
                    )
                )
            data["task"] = task_list
            if x := group_info.get(int(group_id)):
                data["group"] = x
            else:
                continue
            try:
                group_list_result.append(GroupResult(**data))
            except ValidationError:
                pass
        except Exception as e:
            logger.error(f"WEB_UI /webui/group 发生错误 {type(e)}：{e}")
    return Result(code=200, data=group_list_result)


@app.post("/webui/group")
async def _(group: GroupResult, user: User = Depends(token_to_user)) -> Result:
    """
    修改群信息
    """
    group_id = group.group.group_id
    group_manager.set_group_level(group_id, group.level)
    if group.status:
        group_manager.turn_on_group_bot_status(group_id)
    else:
        group_manager.shutdown_group_bot_status(group_id)
    return Result(code=200, data="修改成功！")
