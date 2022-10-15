from nonebot import on_command

from models.user_shop_gold_log import UserShopGoldLog
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.params import CommandArg

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
        使用道具 [序号或道具名称] ?[数量]=1
    * 序号以 ”我的道具“ 为准 *
""".strip()
__plugin_des__ = "商店 - 使用道具"
__plugin_cmd__ = ["使用道具 [序号或道具名称]"]
__plugin_type__ = ('商店',)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店", "使用道具"],
}


use_props = on_command("使用道具", priority=5, block=True, permission=GROUP)


@use_props.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    num = 1
    msg_sp = msg.split()
    if len(msg_sp) > 1 and is_number(msg_sp[-1]) and int(msg_sp[-1]) > 0:
        num = int(msg.split()[-1])
        msg = " ".join(msg.split()[:-1])
    property_ = await BagUser.get_property(event.user_id, event.group_id, True)
    if property_:
        name = None
        if is_number(msg):
            if 0 < int(msg) <= len(property_):
                name = list(property_.keys())[int(msg) - 1]
            else:
                await use_props.finish("仔细看看自己的道具仓库有没有这个道具？", at_sender=True)
        else:
            if msg not in property_.keys():
                await use_props.finish("道具名称错误！", at_sender=True)
            name = msg
        _user_prop_count = property_[name]
        if num > _user_prop_count:
            await use_props.finish(f"道具数量不足，无法使用{num}次！")
        if num > (n := func_manager.get_max_num_limit(name)):
            await use_props.finish(f"该道具单次只能使用 {n} 个！")
        model, kwargs = build_params(bot, event, name, num)
        try:
            await func_manager.run_handle(type_="before_handle", param=model, **kwargs)
        except NotMeetUseConditionsException as e:
            await use_props.finish(e.get_info(), at_sender=True)
        async with db.transaction():
            if await BagUser.delete_property(
                event.user_id, event.group_id, name, num
            ):
                if func_manager.check_send_success_message(name):
                    await use_props.send(f"使用道具 {name} {num} 次成功！", at_sender=True)
                if msg := await effect(bot, event, name, num):
                    await use_props.send(msg, at_sender=True)
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 使用道具 {name} {num} 次成功"
                )
                await UserShopGoldLog.add_shop_log(event.user_id, event.group_id, 1, name, num)
            else:
                await use_props.send(f"使用道具 {name} {num} 次失败！", at_sender=True)
                logger.info(
                    f"USER {event.user_id} GROUP {event.group_id} 使用道具 {name} {num} 次失败"
                )
        await func_manager.run_handle(type_="after_handle", param=model, **kwargs)
    else:
        await use_props.send("您的背包里没有任何的道具噢", at_sender=True)
