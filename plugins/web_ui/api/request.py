from typing import Optional

from fastapi import APIRouter

from configs.config import NICKNAME
from models.group_info import GroupInfo
from services.log import logger
from utils.manager import requests_manager
from utils.utils import get_bot

from ..models.model import RequestResult, Result
from ..models.params import HandleRequest
from ..utils import authentication

router = APIRouter()


@router.get("/get_request", dependencies=[authentication()])
def _(request_type: Optional[str]) -> Result:
    try:
        req_data = requests_manager.get_data()
        req_list = []
        if request_type in ["group", "private"]:
            req_data = req_data[request_type]
            for x in req_data:
                req_data[x]["oid"] = x
                req_list.append(RequestResult(**req_data[x]))
            req_list.reverse()
    except Exception as e:
        logger.error("调用API错误", "/get_request", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(req_list, f"{NICKNAME}带来了最新的数据!")


@router.delete("/clear_request", dependencies=[authentication()])
def _(request_type: Optional[str]) -> Result:
    """
    清空请求
    :param type_: 类型
    """
    requests_manager.clear(request_type)
    return Result.ok(info="成功清除了数据")


@router.post("/handle_request", dependencies=[authentication()])
async def _(parma: HandleRequest) -> Result:
    """
    操作请求
    :param parma: 参数
    """
    try:
        result = "操作成功！"
        flag = 3
        if bot := get_bot():
            if parma.handle == "approve":
                if parma.type == "group":
                    if rid := requests_manager.get_group_id(parma.id):
                        # await GroupInfo.update_or_create(defaults={"group_flag": 1}, )
                        if group := await GroupInfo.get_or_none(group_id=str(rid)):
                            await group.update_or_create(group_flag=1)
                        else:
                            group_info = await bot.get_group_info(group_id=rid)
                            await GroupInfo.update_or_create(
                                group_id=str(group_info["group_id"]),
                                defaults={
                                    "group_name": group_info["group_name"],
                                    "max_member_count": group_info["max_member_count"],
                                    "member_count": group_info["member_count"],
                                    "group_flag": 1,
                                },
                            )
                flag = await requests_manager.approve(bot, parma.id, parma.type)
            elif parma.handle == "refuse":
                flag = await requests_manager.refused(bot, parma.id, parma.type)
            elif parma.handle == "delete":
                requests_manager.delete_request(parma.id, parma.type)
            if parma.handle != "delete":
                if flag == 1:
                    result = "该请求已失效"
                    requests_manager.delete_request(parma.id, parma.type)
                elif flag == 2:
                    result = "未找到此Id"
            return Result.ok(result, "成功处理了请求!")
        return Result.fail("Bot未连接")
    except Exception as e:
        logger.error("调用API错误", "/get_group", e=e)
        return Result.fail(f"{type(e)}: {e}")
