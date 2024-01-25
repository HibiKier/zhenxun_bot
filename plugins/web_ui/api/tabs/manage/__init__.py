import re
from typing import Literal, Optional

import nonebot
from fastapi import APIRouter
from nonebot.adapters.onebot.v11.exception import ActionFailed
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from tortoise.functions import Count
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from configs.config import NICKNAME
from models.ban_user import BanUser
from models.chat_history import ChatHistory
from models.friend_user import FriendUser
from models.group_info import GroupInfo
from models.group_member_info import GroupInfoUser
from models.statistics import Statistics
from services.log import logger
from utils.manager import group_manager, plugin_data_manager, requests_manager
from utils.utils import get_bot

from ....base_model import Result
from ....config import AVA_URL, GROUP_AVA_URL
from ....utils import authentication
from ...logs.log_manager import LOG_STORAGE
from .model import (
    DeleteFriend,
    Friend,
    FriendRequestResult,
    GroupDetail,
    GroupRequestResult,
    GroupResult,
    HandleRequest,
    LeaveGroup,
    Message,
    MessageItem,
    Plugin,
    ReqResult,
    SendMessage,
    Task,
    UpdateGroup,
    UserDetail,
)

ws_router = APIRouter()
router = APIRouter(prefix="/manage")

SUB_PATTERN = r"\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))"

GROUP_PATTERN = r'.*?Message (-?\d*) from (\d*)@\[群:(\d*)] "(.*)"'

PRIVATE_PATTERN = r'.*?Message (-?\d*) from (\d*) "(.*)"'

AT_PATTERN = r'\[CQ:at,qq=(.*)\]'

IMAGE_PATTERN = r'\[CQ:image,.*,url=(.*);.*?\]'

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
                gid = g['group_id']
                g['ava_url'] = GROUP_AVA_URL.format(gid, gid)
                group_list_result.append(GroupResult(**g))
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
        all_task = group_manager.get_task_data().keys()
        if group.task:
            for task in all_task:
                if task in group.task:
                    group_manager.open_group_task(group_id, task)
                else:
                    group_manager.close_group_task(group_id, task)
        group_manager[group_id].close_plugins = group.close_plugins
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
            for f in friend_list:
                f['ava_url'] = AVA_URL.format(f['user_id'])
            return Result.ok([Friend(**f) for f in friend_list if str(f['user_id']) != bot_id], "拿到了新鲜出炉的数据!")
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
def _() -> Result:
    try:
        req_result = ReqResult()
        data = requests_manager.get_data()
        for type_ in requests_manager.get_data():
            for x in data[type_]:
                data[type_][x]["oid"] = x
                data[type_][x]['type'] = type_
                if type_ == "private":
                    data[type_][x]['ava_url'] = AVA_URL.format(data[type_][x]['id'])
                    req_result.friend.append(FriendRequestResult(**data[type_][x]))
                else:
                    gid = data[type_][x]['id']
                    data[type_][x]['ava_url'] = GROUP_AVA_URL.format(gid, gid)
                    req_result.group.append(GroupRequestResult(**data[type_][x]))
        req_result.friend.reverse()
        req_result.group.reverse()
    except Exception as e:
        logger.error("调用API错误", "/get_request", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(req_result, f"{NICKNAME}带来了最新的数据!")


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
            try:
                flag = await requests_manager.refused(bots[bot_id], parma.flag, parma.request_type)  # type: ignore
            except ActionFailed as e:
                requests_manager.delete_request(parma.flag, parma.request_type)
                return Result.warning_("请求失败，可能该请求已失效或请求数据错误...")
            if flag == 1:
                requests_manager.delete_request(parma.flag, parma.request_type)
                return Result.warning_("该请求已失效...")
            elif flag == 2:
                return Result.warning_("未找到此Id请求...")
            return Result.ok(info="成功处理了请求!")
        return Result.warning_("无Bot连接...")
    except Exception as e:
        logger.error("调用API错误", "/refuse_request", e=e)
        return Result.fail(f"{type(e)}: {e}")


@router.post("/delete_request", dependencies=[authentication()], description="忽略请求")
async def _(parma: HandleRequest) -> Result:
    """
    操作请求
    :param parma: 参数
    """
    requests_manager.delete_request(parma.flag, parma.request_type)
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
                if rid := requests_manager.get_group_id(parma.flag):
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
            try:
                await requests_manager.approve(bots[bot_id], parma.flag, parma.request_type)  # type: ignore
                return Result.ok(info="成功处理了请求!")
            except ActionFailed as e:
                requests_manager.delete_request(parma.flag, parma.request_type)
                return Result.warning_("请求失败，可能该请求已失效或请求数据错误...")
        return Result.warning_("无Bot连接...")
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
        return Result.warning_("无Bot连接...")
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



@router.get("/get_friend_detail", dependencies=[authentication()], description="获取好友详情")
async def _(bot_id: str, user_id: str) -> Result:
    if bots := nonebot.get_bots():
        if bot_id in bots:
            if fd := [x for x in await bots[bot_id].get_friend_list() if str(x['user_id']) == user_id]:
                like_plugin_list = (
                    await Statistics.filter(user_id=user_id).annotate(count=Count("id"))
                    .group_by("plugin_name").order_by("-count").limit(5)
                    .values_list("plugin_name", "count")
                )
                like_plugin = {}
                for data in like_plugin_list:
                    name = data[0]
                    if plugin_data := plugin_data_manager.get(data[0]):
                        name = plugin_data.name
                    like_plugin[name] = data[1]
                user = fd[0]
                user_detail = UserDetail(
                    user_id=user_id,
                    ava_url=AVA_URL.format(user_id),
                    nickname=user['nickname'],
                    remark=user['remark'],
                    is_ban=await BanUser.is_ban(user_id),
                    chat_count=await ChatHistory.filter(user_id=user_id).count(),
                    call_count=await Statistics.filter(user_id=user_id).count(),
                    like_plugin=like_plugin,
                )
                return Result.ok(user_detail)
            else:
                return Result.warning_("未添加指定好友...")
    return Result.warning_("无Bot连接...")


@router.get("/get_group_detail", dependencies=[authentication()], description="获取群组详情")
async def _(bot_id: str, group_id: str) -> Result:
    if bots := nonebot.get_bots():
        if bot_id in bots:
            group_info = await bots[bot_id].get_group_info(group_id=int(group_id))
            g = group_manager[group_id]
            if not g:
                return Result.warning_("指定群组未被收录...")
            if group_info:
                like_plugin_list = (
                    await Statistics.filter(group_id=group_id).annotate(count=Count("id"))
                    .group_by("plugin_name").order_by("-count").limit(5)
                    .values_list("plugin_name", "count")
                )
                like_plugin = {}
                for data in like_plugin_list:
                    name = data[0]
                    if plugin_data := plugin_data_manager.get(data[0]):
                        name = plugin_data.name
                    like_plugin[name] = data[1]
                close_plugins = []
                for module in g.close_plugins:
                    module_ = module.replace(":super", "")
                    is_super_block = module.endswith(":super")
                    plugin = Plugin(module=module_, plugin_name=module, is_super_block=is_super_block)
                    if plugin_data := plugin_data_manager.get(module_):
                        plugin.plugin_name = plugin_data.name
                    close_plugins.append(plugin)
                task_list = []
                task_data = group_manager.get_task_data()
                for tn, status in g.group_task_status.items():
                    task_list.append(
                        Task(
                            name=tn,
                            zh_name=task_data.get(tn) or tn,
                            status=status
                        )
                    )
                group_detail = GroupDetail(
                    group_id=group_id,
                    ava_url=GROUP_AVA_URL.format(group_id, group_id),
                    name=group_info['group_name'],
                    member_count=group_info['member_count'],
                    max_member_count=group_info['max_member_count'],
                    chat_count=await ChatHistory.filter(group_id=group_id).count(),
                    call_count=await Statistics.filter(group_id=group_id).count(),
                    like_plugin=like_plugin,
                    level=g.level,
                    status=g.status,
                    close_plugins=close_plugins,
                    task=task_list
                )
                return Result.ok(group_detail)
            else:
                return Result.warning_("未添加指定群组...")
    return Result.warning_("无Bot连接...")


@router.post("/send_message", dependencies=[authentication()], description="获取群组详情")
async def _(param: SendMessage) -> Result:
    if bots := nonebot.get_bots():
        if param.bot_id in bots:
            try:
                if param.user_id:
                    await bots[param.bot_id].send_private_msg(user_id=str(param.user_id), message=param.message)
                else:
                    await bots[param.bot_id].send_group_msg(group_id=str(param.group_id), message=param.message)
            except Exception as e:
                return Result.fail(str(e))
            return Result.ok("发送成功!")
        return Result.warning_("指定Bot未连接...")
    return Result.warning_("无Bot连接...")

MSG_LIST = []

ID2NAME = {}


async def message_handle(sub_log: str, type: Literal["private", "group"]):
    global MSG_LIST, ID2NAME
    pattern = PRIVATE_PATTERN if type == 'private' else GROUP_PATTERN
    msg_id = None
    uid = None
    gid = None
    msg = None
    img_list =  re.findall(IMAGE_PATTERN, sub_log)
    if r := re.search(pattern, sub_log):
        if type == 'private':
            msg_id = r.group(1)
            uid = r.group(2)
            msg = r.group(3)
            if uid not in ID2NAME:
                user = await FriendUser.filter(user_id=uid).first()
                ID2NAME[uid] = user.user_name or user.nickname
        else:
            msg_id = r.group(1)
            uid = r.group(2)
            gid = r.group(3)
            msg = r.group(4)
            if gid not in ID2NAME:
                user = await GroupInfoUser.filter(user_id=uid, group_id=gid).first()
                ID2NAME[uid] = user.user_name or user.nickname
            if at_list := re.findall(AT_PATTERN, msg):
                user_list = await GroupInfoUser.filter(user_id__in=at_list, group_id=gid).all()
                id2name = {u.user_id: (u.user_name or u.nickname) for u in user_list}
                for qq in at_list:
                    msg = re.sub(rf'\[CQ:at,qq={qq}\]', f"@{id2name[qq] or ''}", msg)
    if msg_id in MSG_LIST:
        return
    MSG_LIST.append(msg_id)
    messages = []
    rep = re.split(r'\[CQ:image.*\]', msg)
    if img_list:
        for i in range(len(rep)):
            messages.append(MessageItem(type="text", msg=rep[i]))
            if i < len(img_list):
                messages.append(MessageItem(type="img", msg=img_list[i]))
    else:
        messages = [MessageItem(type="text", msg=x) for x in rep]
    return Message(
            object_id=uid if type == 'private' else gid,
            user_id=uid,
            group_id=gid,
            message=messages,
            name=ID2NAME.get(uid) or "",
            ava_url=AVA_URL.format(uid),
        )

@ws_router.websocket("/chat")
async def _(websocket: WebSocket):
    await websocket.accept()

    async def log_listener(log: str):
        global MSG_LIST, ID2NAME
        sub_log = re.sub(SUB_PATTERN, "", log)
        img_list =  re.findall(IMAGE_PATTERN, sub_log)
        if "message.private.friend" in log:
            if message := await message_handle(sub_log, 'private'):
                await websocket.send_json(message.dict())
        else:
            if r := re.search(GROUP_PATTERN, sub_log):
                if message := await message_handle(sub_log, 'group'):
                    await websocket.send_json(message.dict())
        if len(MSG_LIST) > 30:
            MSG_LIST = MSG_LIST[-1:]
    LOG_STORAGE.listeners.add(log_listener)
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            recv = await websocket.receive()
    except WebSocketDisconnect:
        pass
    finally:
        LOG_STORAGE.listeners.remove(log_listener)
    return