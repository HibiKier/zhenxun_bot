from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from nonebot.typing import T_State
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from .data_source import create_shop_help, add_goods, del_goods, update_goods
from nonebot.permission import SUPERUSER
from utils.utils import get_message_text, is_number
from services.log import logger
import os
import time


__zx_plugin_name__ = "商店"
__plugin_usage__ = """
usage：
    商店项目，这可不是奸商
    指令：
        商店
""".strip()
__plugin_superuser_usage__ = """
usage：
    商品操作
    指令：
        添加商品 [名称]-[价格]-[描述]-?[折扣](小数)-?[限时时间](分钟)
        删除商品 [名称或序号]
        修改商品 -name [名称或序号] -price [价格] -des [描述] -discount [折扣] -time [限时]
        示例：添加商品-昏睡红茶-300-一杯上好的奇怪红茶-0.9-60
        示例：删除商品 2
        示例：修改商品 -name 1 -price 900: 修改序号为1的商品的价格为900
    * 修改商品只需添加需要值即可 *
""".strip()
__plugin_des__ = "商店系统[金币回收计划]"
__plugin_cmd__ = [
    "商店",
    "添加商品 [名称]-[价格]-[描述]-?[折扣](小数)-?[限时时间](分钟) [_superuser]",
    "删除商品 [名称或序号] [_superuser]",
    "修改商品 -name [名称或序号] -price [价格] -des [描述] -discount [折扣] -time [限时] [_superuser]",
]
__plugin_type__ = ('商店',)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店"],
}


shop_help = on_command("商店", priority=5, block=True)

shop_add_goods = on_command("添加商品", priority=5, permission=SUPERUSER, block=True)

shop_del_goods = on_command("删除商品", priority=5, permission=SUPERUSER, block=True)

shop_update_goods = on_command("修改商品", priority=5, permission=SUPERUSER, block=True)


@shop_help.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if not os.path.exists(f"{IMAGE_PATH}/shop_help.png"):
        await create_shop_help()
    await shop_help.send(image("shop_help.png"))


@shop_add_goods.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg:
        msg = msg.split("-")
        if len(msg) < 3:
            await shop_add_goods.finish("商品参数不完全...", at_sender=True)
        if not is_number(msg[1]):
            await shop_add_goods.finish("商品的价格必须是合法数字！", at_sender=True)
        msg[1] = int(msg[1])
        if len(msg) > 3:
            if not is_number(msg[3]):
                await shop_add_goods.finish("商品的折扣要小数啊！", at_sender=True)
            msg[3] = float(msg[3])
        if len(msg) > 4:
            if not is_number(msg[4]):
                await shop_add_goods.finish("商品的限时时间是要写多少分钟噢！", at_sender=True)
            msg[4] = time.time() + int(msg[4]) * 60
        if await add_goods(msg):
            await shop_add_goods.send(f"添加商品 {msg[0]} 成功...", at_sender=True)
            if os.path.exists(f"{IMAGE_PATH}/shop_help.png"):
                os.remove(f"{IMAGE_PATH}/shop_help.png")
            logger.info(f"USER {event.user_id} 上传商品 {msg} 成功")
        else:
            await shop_add_goods.send(f"添加商品 {msg[0]} 失败了...", at_sender=True)
            logger.warning(f"USER {event.user_id} 上传商品 {msg} 失败")


@shop_del_goods.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg:
        name = ""
        id_ = 0
        if is_number(msg):
            id_ = int(msg)
        else:
            name = msg
        rst, goods_name, code = await del_goods(name, id_)
        if code == 200:
            await shop_del_goods.send(f"删除商品 {goods_name} 成功了...", at_sender=True)
            if os.path.exists(f"{IMAGE_PATH}/shop_help.png"):
                os.remove(f"{IMAGE_PATH}/shop_help.png")
            logger.info(f"USER {event.user_id} 删除商品 {goods_name} 成功")
        else:
            await shop_del_goods.send(f"删除商品 {goods_name} 失败了...", at_sender=True)
            logger.info(f"USER {event.user_id} 删除商品 {goods_name} 失败")


@shop_update_goods.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if msg:
        tmp = {}
        msg = msg.split("-")
        for x in msg:
            if x.find("name") != -1:
                tmp["name"] = x.split(" ")[1].strip()
            elif x.find("price") != -1:
                tmp["price"] = x.split(" ")[1].strip()
                if not is_number(tmp["price"]):
                    await shop_update_goods.finish("价格必须是数字啊！", at_sender=True)
                tmp["price"] = int(tmp["price"])
            elif x.find("des") != -1:
                tmp["des"] = x.split(" ")[1].strip()
            elif x.find("discount") != -1:
                tmp["discount"] = x.split(" ")[1].strip()
                if not is_number(tmp["discount"]):
                    await shop_update_goods.finish("折扣必须是数字啊！", at_sender=True)
                tmp["discount"] = float(tmp["discount"])
            elif x.find("time") != -1:
                tmp["time"] = x.split(" ")[1].strip()
                if not is_number(tmp["time"]):
                    await shop_update_goods.finish("限时时间必须是数字啊！", at_sender=True)
                tmp["time"] = time.time() + tmp["time"] * 60
        if not tmp.get("name"):
            await shop_update_goods.finish("未指定商品名称(序号也可)！", at_sender=True)
        if is_number(tmp["name"]):
            tmp["name"] = int(tmp["name"])
        flag, name, text = await update_goods(tmp)
        if flag:
            await shop_update_goods.send(f"修改商品 {name} 成功了...\n{text}", at_sender=True)
            if os.path.exists(f"{IMAGE_PATH}/shop_help.png"):
                os.remove(f"{IMAGE_PATH}/shop_help.png")
            logger.info(f"USER {event.user_id} 修改商品 {name} 数据 {tmp} 成功")
        else:
            await shop_update_goods.send(f"修改商品 {name} 失败了...", at_sender=True)
            logger.info(f"USER {event.user_id} 修改商品 {name} 数据 {tmp} 失败")
