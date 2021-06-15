from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me


super_help = on_command("超级用户帮助", rule=to_me(), priority=1, permission=SUPERUSER, block=True)


@super_help.handle()
async def _(bot: Bot, event: Event, state: T_State):
    result = '''超级用户帮助：
    1.添加/删除管理
    2.查看群组/查看好友
    3.广播 --> 指令:广播-
    4.更新色图
    5.回复 --> 指令:/t 用户 群号
    6.更新cookie --> 指令:更新cookie [cookie]
    7.开启广播通知 --> 指令:开启广播通知 [群号]
    8.退群 --> 指令:退群 群号
    9.自检
    10.更新好友信息
    11.更新群群信息
    12.重载原神/方舟卡池
    13.添加商品 [名称] [价格] [描述] [折扣] [限时时间]
    14.删除商品 [名称(序号)]
    15.修改商品 -name [名称(序号)] -price [价格] -des [描述] -discount [折扣] -time [限时]
    16.节日红包 [金额] [数量] [祝福语](可省) [指定群](可省) [指定群]...'''
    await super_help.finish(result, at_sender=True)



