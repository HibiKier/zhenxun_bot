from models.group_info import GroupInfo
from utils.manager import requests_manager
from utils.utils import get_bot

from ..auth import Depends, User, token_to_user
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
                if rid := requests_manager.get_group_id(parma.id):
                    # await GroupInfo.update_or_create(defaults={"group_flag": 1}, )
                    if group := await GroupInfo.filter(group_id=rid).first():
                        await group.update_or_create(group_flag=1)
                    else:
                        group_info = await bot.get_group_info(group_id=rid)
                        await GroupInfo.update_or_create(
                            group_id=group_info["group_id"],
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
        return Result(code=200, data=result)
