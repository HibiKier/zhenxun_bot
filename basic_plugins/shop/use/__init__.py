from typing import Any, Tuple

from nonebot import on_command, on_regex

from models.user_shop_gold_log import UserShopGoldLog
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.params import CommandArg, RegexGroup

from utils.decorator.shop import NotMeetUseConditionsException
from utils.utils import is_number
from models.bag_user import BagUser
from nonebot.adapters.onebot.v11.permission import GROUP
from services.db_context import db
from .data_source import effect, register_use, func_manager, build_params


__zx_plugin_name__ = "商店 - 使用道具"
__plugin_usage__ = """
usage：
    普通的使用道具
    指令：
        使用道具 [序号或道具名称] ?[数量]=1 ?[其他信息]
        示例：使用道具好感度双倍加持卡         使用道具好感度双倍加持卡
        示例：使用道具1                     使用第一个道具
        示例：使用道具1 10                  使用10个第一个道具       
        示例：使用道具1 1 来点色图           使用第一个道具并附带信息
    * 序号以 ”我的道具“ 为准 *
""".strip()
__plugin_des__ = "商店 - 使用道具"
__plugin_cmd__ = ["使用道具 [序号或道具名称]"]
__plugin_type__ = ("商店",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店", "使用道具"],
}


use_props = on_command(r"使用道具", priority=5, block=True, permission=GROUP)


@use_props.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text()
    num = 1
    text = ""
    prop_n = None
    index = None
    split = msg.split()
    if size := len(split):
        if size == 1:
            prop_n = split[0].strip()
            index = 1
        if size > 1 and is_number(split[1].strip()):
            prop_n = split[0].strip()
            num = int(split[1].strip())
            index = 2
    else:
        await use_props.finish("缺少参数，请查看帮助", at_sender=True)
    if index:
        text = " ".join(split[index:])
    property_ = await BagUser.get_property(event.user_id, event.group_id, True)
    if property_:
        name = None
        if prop_n and is_number(prop_n):
            if 0 < int(prop_n) <= len(property_):
                name = list(property_.keys())[int(prop_n) - 1]
            else:
                await use_props.finish("仔细看看自己的道具仓库有没有这个道具？", at_sender=True)
        else:
            if prop_n not in property_.keys():
                await use_props.finish("道具名称错误！", at_sender=True)
            name = prop_n
        _user_prop_count = property_[name]
        if num > _user_prop_count:
            await use_props.finish(f"道具数量不足，无法使用{num}次！")
        if num > (n := func_manager.get_max_num_limit(name)):
            await use_props.finish(f"该道具单次只能使用 {n} 个！")
        model, kwargs = build_params(bot, event, name, num, text)
        try:
            await func_manager.run_handle(type_="before_handle", param=model, **kwargs)
        except NotMeetUseConditionsException as e:
            await use_props.finish(e.get_info(), at_sender=True)
        async with db.transaction():
            if await BagUser.delete_property(event.user_id, event.group_id, name, num):
                if func_manager.check_send_success_message(name):
                    await use_props.send(f"使用道具 {name} {num} 次成功！", at_sender=True)
                if msg := await effect(bot, event, name, num, text, event.message):
                    await use_props.send(msg, at_sender=True)
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 使用道具 {name} {num} 次成功"
                )
                await UserShopGoldLog.add_shop_log(
                    event.user_id, event.group_id, 1, name, num
                )
            else:
                await use_props.send(f"使用道具 {name} {num} 次失败！", at_sender=True)
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 使用道具 {name} {num} 次失败"
                )
        await func_manager.run_handle(type_="after_handle", param=model, **kwargs)
    else:
        await use_props.send("您的背包里没有任何的道具噢", at_sender=True)
