from fastapi import APIRouter
from pydantic.error_wrappers import ValidationError

from services.log import logger
from utils.manager import group_manager
from utils.utils import get_bot

from ..models.model import Group, GroupResult, Result, Task
from ..models.params import UpdateGroup
from ..utils import authentication

router = APIRouter()


@router.get("/get_group", dependencies=[authentication()])
async def _() -> Result:
    """
    获取群信息
    """
    group_list_result = []
    try:
        group_info = {}
        if bot := get_bot():
            group_list = await bot.get_group_list()
            for g in group_list:
                group_info[g["group_id"]] = Group(**g)
        group_data = group_manager.get_data()
        for group_id in group_data.group_manager:
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
            group_list_result.append(GroupResult(**data))
    except Exception as e:
        logger.error("调用API错误", "/get_group", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(group_list_result, "拿到了新鲜出炉的数据!")


@router.post("/update_group", dependencies=[authentication()])
async def _(group: UpdateGroup) -> Result:
    """
    修改群信息
    """
    try:
        group_id = group.group_id
        group_manager.set_group_level(group_id, group.level)
        if group.status:
            group_manager.turn_on_group_bot_status(group_id)
        else:
            group_manager.shutdown_group_bot_status(group_id)
        group_manager.save()
    except Exception as e:
        logger.error("调用API错误", "/get_group", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(info="已完成记录!")
