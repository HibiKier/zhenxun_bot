from typing import Literal

import nonebot
from fastapi import APIRouter
from pydantic.error_wrappers import ValidationError

from configs.config import NICKNAME
from models.group_info import GroupInfo
from services.log import logger
from utils.manager import group_manager, requests_manager
from utils.utils import get_bot

from ....base_model import Result
from ....utils import authentication
from .model import (
    DeleteFriend,
    Friend,
    FriendRequestResult,
    Group,
    GroupRequestResult,
    GroupResult,
    HandleRequest,
    LeaveGroup,
    Task,
    UpdateGroup,
)

router = APIRouter()


@router.get("/get_group_list", dependencies=[authentication()], description="获取群组列表")
async def _(bot_id: str) -> Result:
    """
    获取群信息
    """
    if bots := nonebot.get_bots():
        if bot_id not in bots:
            return Result.warning_("指定Bot未连接...")
        group_list_result = []
        try:
            group_info = {}
            group_list = await bots[bot_id].get_group_list()
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
            logger.error("调用API错误", "/get_group_list", e=e)
            return Result.fail(f"{type(e)}: {e}")
        return Result.ok(group_list_result, "拿到了新鲜出炉的数据!")
    return Result.warning_("无Bot连接...")


@router.post("/update_group", dependencies=[authentication()], description="修改群组信息")
async def _(group: UpdateGroup) -> Result:
    try:
        group_id = group.group_id
        group_manager.set_group_level(group_id, group.level)
        if group.status:
            group_manager.turn_on_group_bot_status(group_id)
        else:
            group_manager.shutdown_group_bot_status(group_id)
        if group.task_status:
            for task in group.task_status:
                if group.task_status[task]:
                    group_manager.open_group_task(group_id, task)
                else:
                    group_manager.close_group_task(group_id, task)
        group_manager.save()
    except Exception as e:
        logger.error("调用API错误", "/get_group", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(info="已完成记录!")


@router.get("/get_friend_list", dependencies=[authentication()], description="获取好友列表")
async def _(bot_id: str) -> Result:
    """
    获取群信息
    """
    if bots := nonebot.get_bots():
        if bot_id not in bots:
            return Result.warning_("指定Bot未连接...")
        try:
            friend_list = await bots[bot_id].get_friend_list()
            return Result.ok([Friend(**f) for f in friend_list], "拿到了新鲜出炉的数据!")
        except Exception as e:
            logger.error("调用API错误", "/get_group_list", e=e)
            return Result.fail(f"{type(e)}: {e}")
    return Result.warning_("无Bot连接...")


@router.get("/get_request_count", dependencies=[authentication()], description="获取请求数量")
def _() -> Result:
    data = {
        "friend_count": len(requests_manager.get_data().get("private") or []),
        "group_count": len(requests_manager.get_data().get("group") or []),
    }
    return Result.ok(data, f"{NICKNAME}带来了最新的数据!")


@router.get("/get_request_list", dependencies=[authentication()], description="获取请求列表")
def _(request_type: Literal["private", "group"]) -> Result:
    try:
        req_data = requests_manager.get_data().get(request_type) or []
        req_list = []
        for x in req_data:
            req_data[x]["oid"] = x
            if request_type == "private":
                req_list.append(FriendRequestResult(**req_data[x]))
            else:
                req_list.append(GroupRequestResult(**req_data[x]))
        req_list.reverse()
    except Exception as e:
        logger.error("调用API错误", "/get_request", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(req_list, f"{NICKNAME}带来了最新的数据!")


@router.delete("/clear_request", dependencies=[authentication()], description="清空请求列表")
def _(request_type: Literal["private", "group"]) -> Result:
    """
    清空请求
    :param type_: 类型
    """
    requests_manager.clear(request_type)
    return Result.ok(info="成功清除了数据!")


@router.post("/refuse_request", dependencies=[authentication()], description="拒绝请求")
async def _(parma: HandleRequest) -> Result:
    """
    操作请求
    :param parma: 参数
    """
    try:
        if bots := nonebot.get_bots():
            bot_id = parma.bot_id
            if bot_id not in nonebot.get_bots():
                return Result.warning_("指定Bot未连接...")
            flag = await requests_manager.refused(bots[bot_id], parma.id, parma.request_type)  # type: ignore
            if flag == 1:
                requests_manager.delete_request(parma.id, parma.request_type)
                return Result.warning_("该请求已失效...")
            elif flag == 2:
                return Result.warning_("未找到此Id请求...")
            return Result.ok(info="成功处理了请求!")
        return Result.warning_("Bot未连接...")
    except Exception as e:
        logger.error("调用API错误", "/refuse_request", e=e)
        return Result.fail(f"{type(e)}: {e}")


@router.post("/delete_request", dependencies=[authentication()], description="忽略请求")
async def _(parma: HandleRequest) -> Result:
    """
    操作请求
    :param parma: 参数
    """
    requests_manager.delete_request(parma.id, parma.request_type)
    return Result.ok(info="成功处理了请求!")


@router.post("/approve_request", dependencies=[authentication()], description="同意请求")
async def _(parma: HandleRequest) -> Result:
    """
    操作请求
    :param parma: 参数
    """
    try:
        if bots := nonebot.get_bots():
            bot_id = parma.bot_id
            if bot_id not in nonebot.get_bots():
                return Result.warning_("指定Bot未连接...")
            if parma.request_type == "group":
                if rid := requests_manager.get_group_id(parma.id):
                    if group := await GroupInfo.get_or_none(group_id=str(rid)):
                        await group.update_or_create(group_flag=1)
                    else:
                        group_info = await bots[bot_id].get_group_info(group_id=rid)
                        await GroupInfo.update_or_create(
                            group_id=str(group_info["group_id"]),
                            defaults={
                                "group_name": group_info["group_name"],
                                "max_member_count": group_info["max_member_count"],
                                "member_count": group_info["member_count"],
                                "group_flag": 1,
                            },
                        )
            await requests_manager.approve(bots[bot_id], parma.id, parma.request_type)  # type: ignore
            return Result.ok(info="成功处理了请求!")
        return Result.warning_("Bot未连接...")
    except Exception as e:
        logger.error("调用API错误", "/approve_request", e=e)
        return Result.fail(f"{type(e)}: {e}")


@router.post("/leave_group", dependencies=[authentication()], description="退群")
async def _(param: LeaveGroup) -> Result:
    try:
        if bots := nonebot.get_bots():
            bot_id = param.bot_id
            group_list = await bots[bot_id].get_group_list()
            if param.group_id not in [str(g["group_id"]) for g in group_list]:
                return Result.warning_("Bot未在该群聊中...")
            await bots[bot_id].set_group_leave(group_id=param.group_id)
            return Result.ok(info="成功处理了请求!")
        return Result.warning_("Bot未连接...")
    except Exception as e:
        logger.error("调用API错误", "/leave_group", e=e)
        return Result.fail(f"{type(e)}: {e}")


@router.post("/delete_friend", dependencies=[authentication()], description="删除好友")
async def _(param: DeleteFriend) -> Result:
    try:
        if bots := nonebot.get_bots():
            bot_id = param.bot_id
            friend_list = await bots[bot_id].get_friend_list()
            if param.user_id not in [str(g["user_id"]) for g in friend_list]:
                return Result.warning_("Bot未有其好友...")
            await bots[bot_id].delete_friend(user_id=param.user_id)
            return Result.ok(info="成功处理了请求!")
        return Result.warning_("Bot未连接...")
    except Exception as e:
        logger.error("调用API错误", "/delete_friend", e=e)
        return Result.fail(f"{type(e)}: {e}")
