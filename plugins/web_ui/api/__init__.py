from utils.manager import (
    plugins_manager,
    group_manager,
    plugins2settings_manager,
    plugins2cd_manager,
    plugins2block_manager,
    plugins2count_manager,
    requests_manager,
)
from ..auth import token_to_user, Depends, User
from utils.utils import get_matchers, get_bot
from models.group_info import GroupInfo
from pydantic.error_wrappers import ValidationError
from services.log import logger
from ..config import *
import nonebot

app = nonebot.get_app()


plugin_name_list = None


@app.get("/webui/plugins")
def _(type_: Optional[str], user: User = Depends(token_to_user)) -> Result:
    """
    获取插件列表
    :param type_: 类型 normal, superuser, hidden, admin
    """
    global plugin_name_list
    if not plugin_name_list:
        plugin_name_list = [x.plugin_name for x in get_matchers()]
    plugin_list = []
    plugin_data = plugins_manager.get_data()
    for model in plugin_data:
        if model in plugin_name_list:
            data = plugin_data.get(model)
            data["model"] = model
            plugin_name = data.get("plugin_name")
            if (
                (type_ == "hidden" and "[hidden]" not in plugin_name.lower())
                or (type_ == "admin" and "[admin]" not in plugin_name.lower())
                or (type_ == "superuser" and "[superuser]" not in plugin_name.lower())
            ):
                continue
            if type_ == "normal" and (
                "[hidden]" in plugin_name.lower()
                or "[admin]" in plugin_name.lower()
                or "[superuser]" in plugin_name.lower()
            ):
                continue
            data = {"model": model}
            if x := plugin_data.get(model):
                if not x.get("status") and x.get("block_type") in [
                    "group",
                    "private",
                    "all",
                ]:
                    x["block_type"] = (
                        "群聊"
                        if x["block_type"] == "group"
                        else "私聊"
                        if x["block_type"] == "private"
                        else "全部"
                    )
                data["plugin_manager"] = PluginManager(**x)
            if x := plugins2settings_manager.get(model):
                if x.get("cmd") and isinstance(x.get("cmd"), list):
                    x["cmd"] = ",".join(x["cmd"])
                # if isinstance(x["plugin_type"], list):
                #     x["plugin_type"] = x["plugin_type"][0]
                data["plugin_settings"] = PluginSettings(**x)
            if x := plugins2cd_manager.get(model):
                data["cd_limit"] = CdLimit(**x)
            if x := plugins2block_manager.get(model):
                data["block_limit"] = BlockLimit(**x)
            if x := plugins2count_manager.get(model):
                data["count_limit"] = CountLimit(**x)
            # if x := resources_manager.get(model):
            #     data = dict(data, **x)
            plugin_list.append(Plugin(**data))
    return Result(code=200, data=plugin_list)


@app.post("/webui/plugins")
def _(plugin: Plugin, user: User = Depends(token_to_user)) -> Result:
    """
    修改插件信息
    :param plugin: 插件内容
    """
    if plugin.plugin_settings:
        for key, value in plugin.plugin_settings:
            plugins2settings_manager.set_module_data(plugin.model, key, value)
    if plugin.plugin_manager:
        for key, value in plugin.plugin_manager:
            plugins_manager.set_module_data(plugin.model, key, value)
    return Result(code=200)


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
    for group_id in group_data["group_manager"]:
        try:
            task_list = []
            data = group_data["group_manager"][group_id]
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
    return Result(code=200)


@app.get("/webui/request")
def _(type_: Optional[str], user: User = Depends(token_to_user)) -> Result:
    req_data = requests_manager.get_data()
    req_list = []
    if type_ in ["group", "private"]:
        req_data = req_data[type_]
        for x in req_data:
            req_data[x]["oid"] = x
            req_list.append(RequestResult(**req_data[x]))
    return Result(code=200, data=req_list)


@app.delete("/webui/request")
def _(type_: Optional[str], user: User = Depends(token_to_user)) -> Result:
    """
    清空请求
    :param type_: 类型
    """
    requests_manager.clear(type_)
    return Result(code=200)


@app.post("/webui/request")
async def _(parma: RequestParma, user: User = Depends(token_to_user)) -> Result:
    """
    操作请求
    :param parma: 参数
    """
    result = "error"
    if bot := get_bot():
        if parma.handle == "approve":
            if parma.type == "group":
                rid = requests_manager.get_group_id(parma.id)
                if await GroupInfo.get_group_info(rid):
                    await GroupInfo.set_group_flag(rid, 1)
                else:
                    group_info = await bot.get_group_info(group_id=rid)
                    await GroupInfo.add_group_info(
                        rid,
                        group_info["group_name"],
                        group_info["max_member_count"],
                        group_info["member_count"],
                        1,
                    )
            if await requests_manager.approve(bot, parma.id, parma.type):
                result = "ok"
        elif parma.handle == "refuse":
            if await requests_manager.refused(bot, parma.id, parma.type):
                result = "ok"
        elif parma.handle == "delete":
            requests_manager.delete_request(parma.id, parma.type)
            result = "ok"
        return Result(code=200, data=result)
