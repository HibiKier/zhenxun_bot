from ..models.goods_info import GoodsInfo
from utils.image_utils import CreateImg
from utils.utils import is_number
from configs.path_config import IMAGE_PATH
from configs.config import Config
from nonebot import Driver
import nonebot
import time
import os


driver: Driver = nonebot.get_driver()


# 导入内置商品 | 重新生成商店图片
@driver.on_startup
async def init_default_shop_goods():
    if os.path.exists(f"{IMAGE_PATH}/shop_help.png"):
        os.remove(f"{IMAGE_PATH}/shop_help.png")
    if Config.get_config("shop", "IMPORT_DEFAULT_SHOP_GOODS"):
        await add_goods(["好感度双倍加持卡Ⅰ", 30, "下次签到双倍好感度概率 + 10%（谁才是真命天子？）（同类商品将覆盖）"])
        await add_goods(["好感度双倍加持卡Ⅱ", 150, "下次签到双倍好感度概率 + 20%（平平庸庸）（同类商品将覆盖）"])
        await add_goods(["好感度双倍加持卡Ⅲ", 250, "下次签到双倍好感度概率 + 30%（金币才是真命天子！）（同类商品将覆盖）"])


# 创建商店界面
async def create_shop_help():
    goods_lst = await GoodsInfo.get_all_goods()
    tmp = ""
    idx = 1
    for goods in goods_lst:
        tmp += (
            f"{idx}.{goods.goods_name}\t\t售价：{goods.goods_price}金币\n"
            f"\t\t{goods.goods_description}\n"
        )
        idx += 1
    w = 1000
    h = 400 + len(goods_lst) * 40
    h = 1000 if h < 1000 else h
    shop_logo = CreateImg(100, 100, background=f"{IMAGE_PATH}/other/shop_text.png")
    shop = CreateImg(w, h, font_size=20)
    zhenxun_img = CreateImg(525, 581, background=f"{IMAGE_PATH}/zhenxun/toukan_2.png")
    shop.paste(zhenxun_img, (780, 100))
    shop.paste(shop_logo, (450, 30), True)
    shop.text(
        (int((1000 - shop.getsize("注【通过 序号 或者 商品名称 购买】")[0]) / 2), 170),
        "注【通过 序号 或者 商品名称 购买】",
    )
    shop.text((20, 230), tmp[:-1])
    shop.text((20, h - 100), "神秘药水\t\t售价：9999999金币\n\t\t鬼知道会有什么效果~")
    shop.save(f"{IMAGE_PATH}/shop_help.png")


# 添加商品
async def add_goods(msg: list):
    data = {
        "名称": None,
        "价格": None,
        "描述": None,
        "折扣": 1,
        "限时": 0,
    }
    keys = list(data.keys())
    idx = 0
    for x in msg:
        data[keys[idx]] = x
        idx += 1
    return await GoodsInfo.add_goods(
        data["名称"], data["价格"], data["描述"], data["折扣"], data["限时"]
    )


# 删除商品
async def del_goods(name: str, id_: int):
    goods_lst = await GoodsInfo.get_all_goods()
    if id_:
        if id_ < 1 or id_ > len(goods_lst):
            return "序号错误，没有该序号商品...", "", 999
        goods_name = goods_lst[id_ - 1].goods_name
        if await GoodsInfo.delete_goods(goods_name):
            return f"删除商品 {goods_name} 成功！", goods_name, 200
        else:
            return f"删除商品 {goods_name} 失败！", goods_name, 999
    if name:
        if await GoodsInfo.delete_goods(name):
            return f"删除商品 {name} 成功！", name, 200
        else:
            return f"删除商品 {name} 失败！", name, 999


# 更新商品信息
async def update_goods(data: dict):
    goods_lst = await GoodsInfo.get_all_goods()
    if is_number(data["name"]):
        if data["name"] < 1 or data["name"] > len(goods_lst):
            return "序号错误，没有该序号的商品...", "", 999
        goods = goods_lst[data["name"] - 1]
    else:
        goods = await GoodsInfo.get_goods_info(data["name"])
        if not goods:
            return "名称错误，没有该名称的商品...", "", 999
    name = goods.goods_name
    price = goods.goods_price
    des = goods.goods_description
    discount = goods.goods_discount
    limit_time = goods.goods_limit_time
    tmp = ""
    if data.get("price"):
        tmp += f'价格：{price} --> {data["price"]}\n'
        price = data["price"]
    if data.get("des"):
        tmp += f'描述：{des} --> {data["des"]}\n'
        des = data["des"]
    if data.get("discount"):
        tmp += f'折扣：{discount} --> {data["discount"]}\n'
        discount = data["discount"]
    if data.get("time"):
        old_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(limit_time))
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data["time"]))
        tmp += f"折扣：{old_time} --> {new_time}\n"
        limit_time = data["time"]
    return (
        await GoodsInfo.update_goods(name, price, des, discount, limit_time),
        name,
        tmp[:-1],
    )
