from utils.manager import requests_manager
from ..auth import token_to_user, Depends, User
from utils.utils import get_bot
from models.group_info import GroupInfo
from ..config import *


@app.get("/webui/request")
def _(type_: Optional[str], user: User = Depends(token_to_user)) -> Result:
    req_data = requests_manager.get_data()
    req_list = []
    if type_ in ["group", "private"]:
        req_data = req_data[type_]
        for x in req_data:
            req_data[x]["oid"] = x
            req_list.append(RequestResult(**req_data[x]))
        req_list.reverse()
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
    result = "操作成功！"
    flag = 3
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
        return Result(code=200, data=result)
