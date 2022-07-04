from PIL import Image

from models.goods_info import GoodsInfo
from utils.image_utils import BuildImage
from models.sign_group_user import SignGroupUser
from utils.utils import is_number
from configs.path_config import IMAGE_PATH
from typing import Optional, Union, Tuple
from configs.config import Config
from nonebot import Driver
from nonebot.plugin import require
from utils.decorator.shop import shop_register
import nonebot
import time

driver: Driver = nonebot.get_driver()


use = require("use")


@driver.on_startup
async def init_default_shop_goods():
    """
    导入内置的三个商品
    """

    @shop_register(
        name=("好感度双倍加持卡Ⅰ", "好感度双倍加持卡Ⅱ", "好感度双倍加持卡Ⅲ"),
        price=(30, 150, 250),
        des=(
            "下次签到双倍好感度概率 + 10%（谁才是真命天子？）（同类商品将覆盖）",
            "下次签到双倍好感度概率 + 20%（平平庸庸）（同类商品将覆盖）",
            "下次签到双倍好感度概率 + 30%（金币才是真命天子！）（同类商品将覆盖）",
        ),
        load_status=Config.get_config("shop", "IMPORT_DEFAULT_SHOP_GOODS"),
        daily_limit=(10, 20, 30),
        ** {"好感度双倍加持卡Ⅰ_prob": 0.1, "好感度双倍加持卡Ⅱ_prob": 0.2, "好感度双倍加持卡Ⅲ_prob": 0.3},
    )
    async def sign_card(user_id: int, group_id: int, prob: float):
        user = await SignGroupUser.ensure(user_id, group_id)
        await user.update(add_probability=prob).apply()


@driver.on_bot_connect
async def _():
    await shop_register.load_register()


# 创建商店界面
async def create_shop_help() -> str:
    """
    制作商店图片
    :return: 图片base64
    """
    goods_lst = await GoodsInfo.get_all_goods()
    idx = 1
    _dc = {}
    font_h = BuildImage(0, 0).getsize("正")[1]
    h = 10
    _list = []
    for goods in goods_lst:
        if goods.goods_limit_time == 0 or time.time() < goods.goods_limit_time:
            h += len(goods.goods_description.strip().split("\n")) * font_h + 80
            _list.append(goods)
    A = BuildImage(1000, h, color="#f9f6f2")
    current_h = 0
    total_n = 0
    for goods in _list:
        bk = BuildImage(1180, 80, font_size=15, color="#f9f6f2", font="CJGaoDeGuo.otf")
        goods_image = BuildImage(
            600, 80, font_size=20, color="#a29ad6", font="CJGaoDeGuo.otf"
        )
        name_image = BuildImage(
            580, 40, font_size=25, color="#e67b6b", font="CJGaoDeGuo.otf"
        )
        await name_image.atext(
            (15, 0), f"{idx}.{goods.goods_name}", center_type="by_height"
        )
        await name_image.aline((380, -5, 280, 45), "#a29ad6", 5)
        await name_image.atext((390, 0), "售价：", center_type="by_height")
        if goods.goods_discount != 1:
            discount_price = int(goods.goods_discount * goods.goods_price)
            old_price_image = BuildImage(0, 0, plain_text=str(goods.goods_price), font_color=(194, 194, 194), font="CJGaoDeGuo.otf", font_size=15)
            await old_price_image.aline((0, int(old_price_image.h / 2), old_price_image.w + 1, int(old_price_image.h / 2)), (0, 0, 0))
            await name_image.apaste(
                old_price_image, (440, 0), True
            )
            await name_image.atext(
                (440, 15), str(discount_price), (255, 255, 255)
            )
        else:
            await name_image.atext(
                (440, 0), str(goods.goods_price), (255, 255, 255), center_type="by_height"
            )
        await name_image.atext(
            (
                440
                + BuildImage(0, 0, plain_text=str(goods.goods_price), font_size=25).w,
                0,
            ),
            f" 金币",
            center_type="by_height",
        )
        await name_image.acircle_corner(5)
        await goods_image.apaste(name_image, (0, 5), True, center_type="by_width")
        await goods_image.atext((15, 50), f"简介：{goods.goods_description}")
        await goods_image.acircle_corner(20)
        await bk.apaste(goods_image, alpha=True)
        n = 0
        _w = 550
        # 添加限时图标和时间
        if goods.goods_limit_time > 0:
            n += 140
            _limit_time_logo = BuildImage(
                40, 40, background=f"{IMAGE_PATH}/other/time.png"
            )
            await bk.apaste(_limit_time_logo, (_w + 50, 0), True)
            await bk.apaste(
                BuildImage(0, 0, plain_text="限时！", font_size=23, font="CJGaoDeGuo.otf"),
                (_w + 90, 10),
                True,
            )
            limit_time = time.strftime(
                "%Y-%m-%d %H:%M", time.localtime(goods.goods_limit_time)
            ).split()
            y_m_d = limit_time[0]
            _h_m = limit_time[1].split(":")
            h_m = _h_m[0] + "时 " + _h_m[1] + "分"
            await bk.atext((_w + 55, 38), str(y_m_d))
            await bk.atext((_w + 65, 57), str(h_m))
            _w += 140
        if goods.goods_discount != 1:
            n += 140
            _discount_logo = BuildImage(30, 30, background=f"{IMAGE_PATH}/other/discount.png")
            await bk.apaste(_discount_logo, (_w + 50, 10), True)
            await bk.apaste(
                BuildImage(0, 0, plain_text="折扣！", font_size=23, font="CJGaoDeGuo.otf"),
                (_w + 90, 15),
                True,
            )
            await bk.apaste(
                BuildImage(0, 0, plain_text=f"{10 * goods.goods_discount:.1f} 折", font_size=30, font="CJGaoDeGuo.otf", font_color=(85, 156, 75)),
                (_w + 50, 44),
                True,
            )
            _w += 140
        if goods.daily_limit != 0:
            n += 140
            _daily_limit_logo = BuildImage(35, 35, background=f"{IMAGE_PATH}/other/daily_limit.png")
            await bk.apaste(_daily_limit_logo, (_w + 50, 10), True)
            await bk.apaste(
                BuildImage(0, 0, plain_text="限购！", font_size=23, font="CJGaoDeGuo.otf"),
                (_w + 90, 20),
                True,
            )
            await bk.apaste(
                BuildImage(0, 0, plain_text=f"{goods.daily_limit}", font_size=30, font="CJGaoDeGuo.otf"),
                (_w + 72, 45),
                True,
            )
        if total_n < n:
            total_n = n
        if n:
            await bk.aline((550, -1, 550 + n, -1), "#a29ad6", 5)
            await bk.aline((550, 80, 550 + n, 80), "#a29ad6", 5)

        # 添加限时图标和时间
        idx += 1
        await A.apaste(bk, (0, current_h), True)
        current_h += 90
    w = 850
    if total_n:
        w += total_n
    h = A.h + 230 + 100
    h = 1000 if h < 1000 else h
    shop_logo = BuildImage(100, 100, background=f"{IMAGE_PATH}/other/shop_text.png")
    shop = BuildImage(w, h, font_size=20, color="#f9f6f2")
    zx_img = BuildImage(0, 0, background=f"{IMAGE_PATH}/zhenxun/toukan_3.png")
    zx_img.transpose(Image.FLIP_LEFT_RIGHT)
    zx_img.replace_color_tran(((240, 240, 240), (255, 255, 255)), (249, 246, 242))
    await shop.apaste(zx_img, (0, 100))
    shop.paste(A, (20 + zx_img.w, 230))
    await shop.apaste(shop_logo, (450, 30), True)
    shop.text(
        (int((1000 - shop.getsize("注【通过 序号 或者 商品名称 购买】")[0]) / 2), 170),
        "注【通过 序号 或者 商品名称 购买】",
    )
    shop.text((20 + zx_img.w, h - 100), "神秘药水\t\t售价：9999999金币\n\t\t鬼知道会有什么效果~")
    return shop.pic2bs4()


async def register_goods(
    name: str,
    price: int,
    des: str,
    discount: Optional[float] = 1,
    limit_time: Optional[int] = 0,
    daily_limit: Optional[int] = 0,
) -> bool:
    """
    添加商品
    例如：                                                  折扣：可选参数↓  限时时间:可选，单位为小时
        添加商品 name:萝莉酒杯 price:9999 des:普通的酒杯，但是里面.. discount:0.4 limit_time:90
        添加商品 name:可疑的药 price:5 des:效果未知
    :param name: 商品名称
    :param price: 商品价格
    :param des: 商品简介
    :param discount: 商品折扣
    :param limit_time: 商品限时销售时间，单位为小时
    :param daily_limit: 每日购买次数限制
    :return: 是否添加成功
    """
    if not await GoodsInfo.get_goods_info(name):
        limit_time = float(limit_time) if limit_time else limit_time
        discount = discount if discount is not None else 1
        limit_time = (
            int(time.time() + limit_time * 60 * 60)
            if limit_time is not None and limit_time != 0
            else 0
        )
        return await GoodsInfo.add_goods(
            name, int(price), des, float(discount), limit_time, daily_limit
        )
    return False


# 删除商品
async def delete_goods(name: str, id_: int) -> "str, str, int":
    """
    删除商品
    :param name: 商品名称
    :param id_: 商品id
    :return: 删除状况
    """
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
async def update_goods(**kwargs) -> Tuple[bool, str, str]:
    """
    更新商品信息
    :param kwargs: kwargs
    :return: 更新状况
    """
    if kwargs:
        goods_lst = await GoodsInfo.get_all_goods()
        if is_number(kwargs["name"]):
            if int(kwargs["name"]) < 1 or int(kwargs["name"]) > len(goods_lst):
                return False, "序号错误，没有该序号的商品...", ""
            goods = goods_lst[int(kwargs["name"]) - 1]
        else:
            goods = await GoodsInfo.get_goods_info(kwargs["name"])
            if not goods:
                return False, "名称错误，没有该名称的商品...", ""
        name: str = goods.goods_name
        price = goods.goods_price
        des = goods.goods_description
        discount = goods.goods_discount
        limit_time = goods.goods_limit_time
        daily_limit = goods.daily_limit
        new_time = 0
        tmp = ""
        if kwargs.get("price"):
            tmp += f'价格：{price} --> {kwargs["price"]}\n'
            price = kwargs["price"]
        if kwargs.get("des"):
            tmp += f'描述：{des} --> {kwargs["des"]}\n'
            des = kwargs["des"]
        if kwargs.get("discount"):
            tmp += f'折扣：{discount} --> {kwargs["discount"]}\n'
            discount = kwargs["discount"]
        if kwargs.get("limit_time"):
            kwargs["limit_time"] = float(kwargs["limit_time"])
            new_time = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(time.time() + kwargs["limit_time"] * 60 * 60),
            ) if kwargs["limit_time"] != 0 else 0
            tmp += f"限时至： {new_time}\n" if new_time else "取消了限时\n"
            limit_time = kwargs["limit_time"]
        if kwargs.get("daily_limit"):
            tmp += f'每日购买限制：{daily_limit} --> {kwargs["daily_limit"]}\n' if daily_limit else "取消了购买限制\n"
            daily_limit = int(kwargs["daily_limit"])
        await GoodsInfo.update_goods(
            name,
            int(price),
            des,
            float(discount),
            int(
                time.time() + limit_time * 60 * 60
                if limit_time != 0 and new_time
                else 0
            ),
            daily_limit
        )
        return True, name, tmp[:-1],


def parse_goods_info(msg: str) -> Union[dict, str]:
    """
    解析格式数据
    :param msg: 消息
    :return: 解析完毕的数据data
    """
    if "name:" not in msg:
        return "必须指定修改的商品名称或序号！"
    data = {}
    for x in msg.split():
        sp = x.split(":", maxsplit=1)
        if str(sp[1]).strip():
            sp[1] = sp[1].strip()
            if sp[0] == "name":
                data["name"] = sp[1]
            elif sp[0] == "price":
                if not is_number(sp[1]) or int(sp[1]) < 0:
                    return "price参数不合法，必须大于等于0！"
                data["price"] = sp[1]
            elif sp[0] == "des":
                data["des"] = sp[1]
            elif sp[0] == "discount":
                if not is_number(sp[1]) or float(sp[1]) < 0:
                    return "discount参数不合法，必须大于0！"
                data["discount"] = sp[1]
            elif sp[0] == "limit_time":
                if not is_number(sp[1]) or float(sp[1]) < 0:
                    return "limit_time参数不合法，必须为数字且大于0！"
                data["limit_time"] = sp[1]
            elif sp[0] == "daily_limit":
                if not is_number(sp[1]) or float(sp[1]) < 0:
                    return "daily_limit参数不合法，必须为数字且大于0！"
                data["daily_limit"] = sp[1]
    return data
