from .data_source import create_shop_help, delete_goods, update_goods, register_goods, parse_goods_info
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot import on_command
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from nonebot.permission import SUPERUSER
from utils.utils import is_number
from nonebot.params import CommandArg
from nonebot.plugin import export
from services.log import logger
import os


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
        添加商品 name:[名称] price:[价格] des:[描述] ?discount:[折扣](小数) ?limit_time:[限时时间](小时)
        删除商品 [名称或序号]
        修改商品 name:[名称或序号] price:[价格] des:[描述] discount:[折扣] limit_time:[限时]
        示例：添加商品 name:萝莉酒杯 price:9999 des:普通的酒杯，但是里面.. discount:0.4 limit_time:90
        示例：添加商品 name:可疑的药 price:5 des:效果未知
        示例：删除商品 2
        示例：修改商品 name:1 price:900   修改序号为1的商品的价格为900
    * 修改商品只需添加需要值即可 *
""".strip()
__plugin_des__ = "商店系统[金币回收计划]"
__plugin_cmd__ = [
    "商店",
    "添加商品 name:[名称] price:[价格] des:[描述] ?discount:[折扣](小数) ?limit_time:[限时时间](小时)) [_superuser]",
    "删除商品 [名称或序号] [_superuser]",
    "修改商品 name:[名称或序号] price:[价格] des:[描述] discount:[折扣] limit_time:[限时] [_superuser]",
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
__plugin_block_limit__ = {
    "limit_type": "group"
}

# 导出方法供其他插件使用
export = export()
export.register_goods = register_goods
export.delete_goods = delete_goods
export.update_goods = update_goods

shop_help = on_command("商店", priority=5, block=True)

shop_add_goods = on_command("添加商品", priority=5, permission=SUPERUSER, block=True)

shop_del_goods = on_command("删除商品", priority=5, permission=SUPERUSER, block=True)

shop_update_goods = on_command("修改商品", priority=5, permission=SUPERUSER, block=True)


@shop_help.handle()
async def _():
    await shop_help.send(image(b64=await create_shop_help()))


@shop_add_goods.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        data = parse_goods_info(msg)
        if isinstance(data, str):
            await shop_add_goods.finish(data)
        if not data.get("name") or not data.get("price") or not data.get("des"):
            await shop_add_goods.finish("name:price:des 参数不可缺少！")
        if await register_goods(**data):
            await shop_add_goods.send(f"添加商品 {data['name']} 成功！\n"
                                      f"名称：{data['name']}\n"
                                      f"价格：{data['price']}金币\n"
                                      f"简介：{data['des']}\n"
                                      f"折扣：{data.get('discount')}\n"
                                      f"限时：{data.get('limit_time')}", at_sender=True)
            logger.info(f"USER {event.user_id} 添加商品 {msg} 成功")
        else:
            await shop_add_goods.send(f"添加商品 {msg} 失败了...", at_sender=True)
            logger.warning(f"USER {event.user_id} 添加商品 {msg} 失败")


@shop_del_goods.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        name = ""
        id_ = 0
        if is_number(msg):
            id_ = int(msg)
        else:
            name = msg
        rst, goods_name, code = await delete_goods(name, id_)
        if code == 200:
            await shop_del_goods.send(f"删除商品 {goods_name} 成功了...", at_sender=True)
            if os.path.exists(f"{IMAGE_PATH}/shop_help.png"):
                os.remove(f"{IMAGE_PATH}/shop_help.png")
            logger.info(f"USER {event.user_id} 删除商品 {goods_name} 成功")
        else:
            await shop_del_goods.send(f"删除商品 {goods_name} 失败了...", at_sender=True)
            logger.info(f"USER {event.user_id} 删除商品 {goods_name} 失败")


@shop_update_goods.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        data = parse_goods_info(msg)
        if isinstance(data, str):
            await shop_add_goods.finish(data)
        if not data.get("name"):
            await shop_add_goods.finish("name 参数不可缺少！")
        flag, name, text = await update_goods(**data)
        if flag:
            await shop_update_goods.send(f"修改商品 {name} 成功了...\n{text}", at_sender=True)
            logger.info(f"USER {event.user_id} 修改商品 {name} 数据 {text} 成功")
        else:
            await shop_update_goods.send(f"修改商品 {name} 失败了...", at_sender=True)
            logger.info(f"USER {event.user_id} 修改商品 {name} 数据 {text} 失败")

