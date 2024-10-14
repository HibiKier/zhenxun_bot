import nonebot
from fastapi import APIRouter
from tortoise.functions import Count
from fastapi.responses import JSONResponse
from nonebot.adapters.onebot.v11 import ActionFailed

from zhenxun.services.log import logger
from zhenxun.configs.config import BotConfig
from zhenxun.models.task_info import TaskInfo
from zhenxun.models.fg_request import FgRequest
from zhenxun.models.statistics import Statistics
from zhenxun.utils.platform import PlatformUtils
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.utils.exception import NotFoundError
from zhenxun.models.chat_history import ChatHistory
from zhenxun.models.group_console import GroupConsole
from zhenxun.utils.enum import RequestType, RequestHandleType

from ....base_model import Result
from ....utils import authentication
from ....config import AVA_URL, GROUP_AVA_URL
from .model import (
    Task,
    Friend,
    Plugin,
    ReqResult,
    LeaveGroup,
    UserDetail,
    GroupDetail,
    GroupResult,
    SendMessage,
    UpdateGroup,
    ClearRequest,
    DeleteFriend,
    HandleRequest,
    GroupRequestResult,
    FriendRequestResult,
)

router = APIRouter(prefix="/manage")


@router.get(
    "/get_group_list",
    dependencies=[authentication()],
    response_model=Result[list[GroupResult]],
    response_class=JSONResponse,
    description="获取群组列表",
)
async def _(bot_id: str) -> Result:
    """
    获取群信息
    """
    if not (bots := nonebot.get_bots()):
        return Result.warning_("无Bot连接...")
    if bot_id not in bots:
        return Result.warning_("指定Bot未连接...")
    group_list_result = []
    try:
        group_list = await bots[bot_id].get_group_list()
        for g in group_list:
            gid = g["group_id"]
            g["ava_url"] = GROUP_AVA_URL.format(gid, gid)
            group_list_result.append(GroupResult(**g))
    except Exception as e:
        logger.error("调用API错误", "/get_group_list", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(group_list_result, "拿到了新鲜出炉的数据!")


@router.post(
    "/update_group",
    dependencies=[authentication()],
    response_model=Result[str],
    response_class=JSONResponse,
    description="修改群组信息",
)
async def _(group: UpdateGroup) -> Result[str]:
    try:
        group_id = group.group_id
        if db_group := await GroupConsole.get_group(group_id):
            task_list = await TaskInfo.all().values_list("module", flat=True)
            db_group.level = group.level
            db_group.status = group.status
            if group.close_plugins:
                group.close_plugins = [f"<{module}" for module in group.close_plugins]
                db_group.block_plugin = ",".join(group.close_plugins) + ","
            if group.task:
                if block_task := [t for t in task_list if t not in group.task]:
                    block_task = [f"<{module}" for module in block_task]
                    db_group.block_task = ",".join(block_task) + ","  # type: ignore
            await db_group.save(
                update_fields=["level", "status", "block_plugin", "block_task"]
            )
    except Exception as e:
        logger.error("调用API错误", "/get_group", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(info="已完成记录!")


@router.get(
    "/get_friend_list",
    dependencies=[authentication()],
    response_model=Result[list[Friend]],
    response_class=JSONResponse,
    description="获取好友列表",
)
async def _(bot_id: str) -> Result[list[Friend]]:
    """
    获取群信息
    """
    if bots := nonebot.get_bots():
        if bot_id not in bots:
            return Result.warning_("指定Bot未连接...")
        try:
            platform = PlatformUtils.get_platform(bots[bot_id])
            if platform != "qq":
                return Result.warning_("该平台暂不支持该功能...")
            friend_list = await bots[bot_id].get_friend_list()
            for f in friend_list:
                f["ava_url"] = AVA_URL.format(f["user_id"])
            return Result.ok(
                [Friend(**f) for f in friend_list if str(f["user_id"]) != bot_id],
                "拿到了新鲜出炉的数据!",
            )
        except Exception as e:
            logger.error("调用API错误", "/get_group_list", e=e)
            return Result.fail(f"{type(e)}: {e}")
    return Result.warning_("无Bot连接...")


@router.get(
    "/get_request_count",
    dependencies=[authentication()],
    response_model=Result[dict[str, int]],
    response_class=JSONResponse,
    description="获取请求数量",
)
async def _() -> Result[dict[str, int]]:
    f_count = await FgRequest.filter(
        request_type=RequestType.FRIEND, handle_type__isnull=True
    ).count()
    g_count = await FgRequest.filter(
        request_type=RequestType.GROUP, handle_type__isnull=True
    ).count()
    data = {
        "friend_count": f_count,
        "group_count": g_count,
    }
    return Result.ok(data, f"{BotConfig.self_nickname}带来了最新的数据!")


@router.get(
    "/get_request_list",
    dependencies=[authentication()],
    response_model=Result[ReqResult],
    response_class=JSONResponse,
    description="获取请求列表",
)
async def _() -> Result[ReqResult]:
    try:
        req_result = ReqResult()
        data_list = await FgRequest.filter(handle_type__isnull=True).all()
        for req in data_list:
            if req.request_type == RequestType.FRIEND:
                req_result.friend.append(
                    FriendRequestResult(
                        oid=req.id,
                        bot_id=req.bot_id,
                        id=req.user_id,
                        flag=req.flag,
                        nickname=req.nickname,
                        comment=req.comment,
                        ava_url=AVA_URL.format(req.user_id),
                        type=str(req.request_type).lower(),
                    )
                )
            else:
                req_result.group.append(
                    GroupRequestResult(
                        oid=req.id,
                        bot_id=req.bot_id,
                        id=req.user_id,
                        flag=req.flag,
                        nickname=req.nickname,
                        comment=req.comment,
                        ava_url=GROUP_AVA_URL.format(req.group_id, req.group_id),
                        type=str(req.request_type).lower(),
                        invite_group=req.group_id,
                        group_name=None,
                    )
                )
        req_result.friend.reverse()
        req_result.group.reverse()
    except Exception as e:
        logger.error("调用API错误", "/get_request", e=e)
        return Result.fail(f"{type(e)}: {e}")
    return Result.ok(req_result, f"{BotConfig.self_nickname}带来了最新的数据!")


@router.post(
    "/clear_request",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    description="清空请求列表",
)
async def _(cr: ClearRequest) -> Result:
    await FgRequest.filter(
        handle_type__isnull=True, request_type=cr.request_type
    ).update(handle_type=RequestHandleType.IGNORE)
    return Result.ok(info="成功清除了数据!")


@router.post(
    "/refuse_request",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    description="拒绝请求",
)
async def _(parma: HandleRequest) -> Result:
    try:
        if bots := nonebot.get_bots():
            bot_id = parma.bot_id
            if bot_id not in nonebot.get_bots():
                return Result.warning_("指定Bot未连接...")
            try:
                await FgRequest.refused(bots[bot_id], parma.id)
            except ActionFailed:
                await FgRequest.expire(parma.id)
                return Result.warning_("请求失败，可能该请求已失效或请求数据错误...")
            except NotFoundError:
                return Result.warning_("未找到此Id请求...")
            return Result.ok(info="成功处理了请求!")
        return Result.warning_("无Bot连接...")
    except Exception as e:
        logger.error("调用API错误", "/refuse_request", e=e)
        return Result.fail(f"{type(e)}: {e}")


@router.post(
    "/delete_request",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    description="忽略请求",
)
async def _(parma: HandleRequest) -> Result:
    await FgRequest.ignore(parma.id)
    return Result.ok(info="成功处理了请求!")


@router.post(
    "/approve_request",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    description="同意请求",
)
async def _(parma: HandleRequest) -> Result:
    try:
        if bots := nonebot.get_bots():
            bot_id = parma.bot_id
            if bot_id not in nonebot.get_bots():
                return Result.warning_("指定Bot未连接...")
            if not (req := await FgRequest.get_or_none(id=parma.id)):
                return Result.warning_("未找到此Id请求...")
            if req.request_type == RequestType.GROUP:
                if group := await GroupConsole.get_group(group_id=req.group_id):
                    group.group_flag = 1
                    await group.save(update_fields=["group_flag"])
                else:
                    await GroupConsole.update_or_create(
                        group_id=req.group_id,
                        defaults={"group_flag": 1},
                    )
            try:
                await FgRequest.approve(bots[bot_id], parma.id)
                return Result.ok(info="成功处理了请求!")
            except ActionFailed:
                await FgRequest.expire(parma.id)
                return Result.warning_("请求失败，可能该请求已失效或请求数据错误...")
        return Result.warning_("无Bot连接...")
    except Exception as e:
        logger.error("调用API错误", "/approve_request", e=e)
        return Result.fail(f"{type(e)}: {e}")


@router.post(
    "/leave_group",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    description="退群",
)
async def _(param: LeaveGroup) -> Result:
    try:
        if bots := nonebot.get_bots():
            bot_id = param.bot_id
            platform = PlatformUtils.get_platform(bots[bot_id])
            if platform != "qq":
                return Result.warning_("该平台不支持退群操作...")
            group_list = await bots[bot_id].get_group_list()
            if param.group_id not in [str(g["group_id"]) for g in group_list]:
                return Result.warning_("Bot未在该群聊中...")
            await bots[bot_id].set_group_leave(group_id=param.group_id)
            return Result.ok(info="成功处理了请求!")
        return Result.warning_("无Bot连接...")
    except Exception as e:
        logger.error("调用API错误", "/leave_group", e=e)
        return Result.fail(f"{type(e)}: {e}")


@router.post(
    "/delete_friend",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    description="删除好友",
)
async def _(param: DeleteFriend) -> Result:
    try:
        if bots := nonebot.get_bots():
            bot_id = param.bot_id
            platform = PlatformUtils.get_platform(bots[bot_id])
            if platform != "qq":
                return Result.warning_("该平台不支持删除好友操作...")
            friend_list = await bots[bot_id].get_friend_list()
            if param.user_id not in [str(g["user_id"]) for g in friend_list]:
                return Result.warning_("Bot未有其好友...")
            await bots[bot_id].delete_friend(user_id=param.user_id)
            return Result.ok(info="成功处理了请求!")
        return Result.warning_("Bot未连接...")
    except Exception as e:
        logger.error("调用API错误", "/delete_friend", e=e)
        return Result.fail(f"{type(e)}: {e}")


@router.get(
    "/get_friend_detail",
    dependencies=[authentication()],
    response_model=Result[UserDetail],
    response_class=JSONResponse,
    description="获取好友详情",
)
async def _(bot_id: str, user_id: str) -> Result[UserDetail]:
    if bots := nonebot.get_bots():
        if bot_id in bots:
            if fd := [
                x
                for x in await bots[bot_id].get_friend_list()
                if str(x["user_id"]) == user_id
            ]:
                like_plugin_list = (
                    await Statistics.filter(user_id=user_id)
                    .annotate(count=Count("id"))
                    .group_by("plugin_name")
                    .order_by("-count")
                    .limit(5)
                    .values_list("plugin_name", "count")
                )
                like_plugin = {}
                module_list = [x[0] for x in like_plugin_list]
                plugins = await PluginInfo.filter(module__in=module_list).all()
                module2name = {p.module: p.name for p in plugins}
                for data in like_plugin_list:
                    name = module2name.get(data[0]) or data[0]
                    like_plugin[name] = data[1]
                user = fd[0]
                user_detail = UserDetail(
                    user_id=user_id,
                    ava_url=AVA_URL.format(user_id),
                    nickname=user["nickname"],
                    remark=user["remark"],
                    is_ban=await BanConsole.is_ban(user_id),
                    chat_count=await ChatHistory.filter(user_id=user_id).count(),
                    call_count=await Statistics.filter(user_id=user_id).count(),
                    like_plugin=like_plugin,
                )
                return Result.ok(user_detail)
            else:
                return Result.warning_("未添加指定好友...")
    return Result.warning_("无Bot连接...")


@router.get(
    "/get_group_detail",
    dependencies=[authentication()],
    response_model=Result[GroupDetail],
    response_class=JSONResponse,
    description="获取群组详情",
)
async def _(bot_id: str, group_id: str) -> Result[GroupDetail]:
    if not (bots := nonebot.get_bots()):
        return Result.warning_("无Bot连接...")
    if bot_id not in bots:
        return Result.warning_("未添加指定群组...")
    group = await GroupConsole.get_or_none(group_id=group_id)
    if not group:
        return Result.warning_("指定群组未被收录...")
    like_plugin_list = (
        await Statistics.filter(group_id=group_id)
        .annotate(count=Count("id"))
        .group_by("plugin_name")
        .order_by("-count")
        .limit(5)
        .values_list("plugin_name", "count")
    )
    like_plugin = {}
    plugins = await PluginInfo.get_plugins()
    module2name = {p.module: p.name for p in plugins}
    for data in like_plugin_list:
        name = module2name.get(data[0]) or data[0]
        like_plugin[name] = data[1]
    close_plugins: list[Plugin] = []
    if group.block_plugin:
        for module in group.block_plugin.replace("<", "").split(","):
            if module:
                plugin = Plugin(
                    module=module,
                    plugin_name=module,
                    is_super_block=False,
                )
                plugin.plugin_name = module2name.get(module) or module
                close_plugins.append(plugin)
    exists_modules = [p.module for p in close_plugins]
    if group.superuser_block_plugin:
        for module in group.superuser_block_plugin.replace("<", "").split(","):
            if module and module not in exists_modules:
                plugin = Plugin(
                    module=module,
                    plugin_name=module,
                    is_super_block=True,
                )
                plugin.plugin_name = module2name.get(module) or module
                close_plugins.append(plugin)
    all_task = await TaskInfo.annotate().values_list("module", "name")
    task_module2name = {x[0]: x[1] for x in all_task}
    task_list = []
    if group.block_task or group.superuser_block_plugin:
        sbp = group.superuser_block_plugin.replace("<", "").split(",")
        split_task = group.block_task.replace("<", "").split(",")
        for task in all_task:
            task_list.append(
                Task(
                    name=task[0],
                    zh_name=task_module2name.get(task[0]) or task[0],
                    status=task[0] not in split_task and task[0] not in sbp,
                    is_super_block=task[0] in sbp,
                )
            )
    else:
        for task in all_task:
            task_list.append(
                Task(
                    name=task[0],
                    zh_name=task_module2name.get(task[0]) or task[0],
                    status=True,
                    is_super_block=False,
                )
            )
    group_detail = GroupDetail(
        group_id=group_id,
        ava_url=GROUP_AVA_URL.format(group_id, group_id),
        name=group.group_name,
        member_count=group.member_count,
        max_member_count=group.max_member_count,
        chat_count=await ChatHistory.filter(group_id=group_id).count(),
        call_count=await Statistics.filter(group_id=group_id).count(),
        like_plugin=like_plugin,
        level=group.level,
        status=group.status,
        close_plugins=close_plugins,
        task=task_list,
    )
    return Result.ok(group_detail)


@router.post(
    "/send_message",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    description="获取群组详情",
)
async def _(param: SendMessage) -> Result:
    if not (bots := nonebot.get_bots()):
        return Result.warning_("无Bot连接...")
    if param.bot_id in bots:
        platform = PlatformUtils.get_platform(bots[param.bot_id])
        if platform != "qq":
            return Result.warning_("暂不支持该平台...")
        try:
            if param.user_id:
                await bots[param.bot_id].send_private_msg(
                    user_id=str(param.user_id), message=param.message
                )
            else:
                await bots[param.bot_id].send_group_msg(
                    group_id=str(param.group_id), message=param.message
                )
        except Exception as e:
            return Result.fail(str(e))
        return Result.ok("发送成功!")
    return Result.warning_("指定Bot未连接...")
