from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.typing import T_State
from models.bag_user import UserBag
from nonebot.adapters.cqhttp.permission import GROUP


__plugin_name__ = '我的金币'


my_gold = on_command("我的金币", priority=5, block=True, permission=GROUP)


@my_gold.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await my_gold.finish(await UserBag.get_my_total_gold(event.user_id, event.group_id))










