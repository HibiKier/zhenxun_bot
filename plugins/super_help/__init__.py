from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from utils.image_utils import CreateImg
from configs.path_config import IMAGE_PATH
from utils.message_builder import image


result = """超级用户帮助：
*：可多个类型参数   ？：可省略参数
    1.添加/删除管理 [at] [level]
    2.查看群组/查看好友
    3.广播- [msg]
    4.更新色图
    5./t命令帮助
    6.更新/设置cookie [cookie]
    7.开启/关闭广播通知 [群号]
    8.退群 [群号]
    9.自检
    10.更新价格/更加图片 [武器箱]
    11.更新好友信息
    12.更新群群信息
    13.重载原神/方舟/赛马娘/坎公骑冠剑卡池
    14.添加商品 [名称]-[价格]-[描述]-[折扣]-[限时时间]
    15.删除商品 [名称(序号)]
    16.修改商品 -name [名称(序号)] -price [价格] -des [描述] -discount [折扣] -time [限时]
    17.节日红包 [金额] [数量] [祝福语](可省) *?[指定群
    18.更新原神今日素材
    19.更新原神资源信息
    20.添加pix关键词/uid/pid *[关键词/uid/pid] ?[-f](强制通过不检测)
    21.通过/取消pix关键词 [keyword/pid:pid/uid:uid]
    22.删除pix关键词 [keyword/uid/pid:pid]
    23.更新pix关键词 [keyword/pid:pid/uid:uid] [num]
    24.删除pix图片 *[pid] ?[-b](同时加入黑名单)
    25.查看pix图库 [keyword]
    26.pix检测更新 [update]
    27.检查更新真寻
    28.真寻重启
    29.添加/删除群白名单 *[群号]
    30.关闭[功能] ?[群号/private/group](有群号时禁用指定群)"""

height = len(result.split('\n')) * 24
A = CreateImg(1000, height, font_size=20)
A.text((10, 10), result)
A.save(f'{IMAGE_PATH}/super_help.png')

super_help = on_command(
    "超级用户帮助", rule=to_me(), priority=1, permission=SUPERUSER, block=True
)


@super_help.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await super_help.finish(image('super_help.png'), at_sender=True)
