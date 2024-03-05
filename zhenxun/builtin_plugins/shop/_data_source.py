import asyncio
import inspect
import time
from types import MappingProxyType
from typing import Any, Callable, Dict, Literal

from nonebot.adapters import Bot, Event
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_saa import MessageFactory
from nonebot_plugin_session import EventSession
from pydantic import BaseModel, create_model

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.models.goods_info import GoodsInfo
from zhenxun.models.user_console import UserConsole
from zhenxun.models.user_gold_log import UserGoldLog
from zhenxun.models.user_props_log import UserPropsLog
from zhenxun.services.log import logger
from zhenxun.utils.enum import GoldHandle, PropHandle
from zhenxun.utils.image_utils import BuildImage, ImageTemplate, text2image

ICON_PATH = IMAGE_PATH / "shop_icon"


class Goods(BaseModel):

    name: str
    """商品名称"""
    before_handle: list[Callable] = []
    """使用前函数"""
    after_handle: list[Callable] = []
    """使用后函数"""
    func: Callable | None = None
    """使用函数"""
    params: Any = None
    """参数"""
    send_success_msg: bool = True
    """使用成功是否发送消息"""
    max_num_limit: int = 1
    """单次使用最大次数"""
    model: Any = None
    """model"""
    session: EventSession | None = None
    """EventSession"""


class ShopParam(BaseModel):

    goods_name: str
    """商品名称"""
    user_id: int
    """用户id"""
    group_id: int
    """群聊id"""
    bot: Any
    """bot"""
    event: Event
    """event"""
    num: int
    """道具单次使用数量"""
    text: str
    """text"""
    send_success_msg: bool = True
    """是否发送使用成功信息"""
    max_num_limit: int = 1
    """单次使用最大次数"""
    session: EventSession | None = None
    """EventSession"""


class ShopManage:

    uuid2goods: Dict[str, Goods] = {}

    @classmethod
    def __build_params(
        cls,
        bot: Bot,
        event: Event,
        session: EventSession,
        message: UniMsg,
        goods: Goods,
        num: int,
        text: str,
    ) -> tuple[ShopParam, Dict[str, Any]]:
        """构造参数

        参数:
            bot: bot
            event: event
            goods_name: 商品名称
            num: 数量
            text: 其他信息
        """
        _kwargs = goods.params
        model = goods.model(
            **{
                "goods_name": goods.name,
                "bot": bot,
                "event": event,
                "user_id": session.id1,
                "group_id": session.id3 or session.id2,
                "num": num,
                "text": text,
                "session": session,
            }
        )
        return model, {
            **_kwargs,
            "_bot": bot,
            "event": event,
            "user_id": session.id1,
            "group_id": session.id3 or session.id2,
            "num": num,
            "text": text,
            "goods_name": goods.name,
        }

    @classmethod
    def __parse_args(
        cls,
        args: MappingProxyType,
        param: ShopParam,
        session: EventSession,
        message: UniMsg,
        **kwargs,
    ) -> list[Any]:
        """解析参数

        参数:
            args: MappingProxyType
            param: ShopParam

        返回:
            list[Any]: 参数
        """
        param_list = []
        _bot = param.bot
        param.bot = None
        param_json = param.dict()
        param_json["bot"] = _bot
        for par in args.keys():
            if par in ["shop_param"]:
                param_list.append(param)
            elif par in ["session"]:
                param_list.append(session)
            elif par in ["message"]:
                param_list.append(message)
            elif par not in ["args", "kwargs"]:
                param_list.append(param_json.get(par))
                if kwargs.get(par) is not None:
                    del kwargs[par]
        return param_list

    @classmethod
    async def run_before_after(
        cls,
        goods: Goods,
        param: ShopParam,
        run_type: Literal["after", "before"],
        **kwargs,
    ):
        """运行使用前使用后函数

        参数:
            goods: Goods
            param: 参数
            run_type: 运行类型
        """
        fun_list = goods.before_handle if run_type == "before" else goods.after_handle
        if fun_list:
            for func in fun_list:
                args = inspect.signature(func).parameters
                if args and list(args.keys())[0] != "kwargs":
                    if asyncio.iscoroutinefunction(func):
                        await func(*cls.__parse_args(args, param, **kwargs))
                    else:
                        func(*cls.__parse_args(args, param, **kwargs))
                else:
                    if asyncio.iscoroutinefunction(func):
                        await func(**kwargs)
                    else:
                        func(**kwargs)

    @classmethod
    async def __run(
        cls,
        goods: Goods,
        param: ShopParam,
        session: EventSession,
        message: UniMsg,
        **kwargs,
    ) -> str | MessageFactory | None:
        """运行道具函数

        参数:
            goods: Goods
            param: ShopParam

        返回:
            str | MessageFactory | None: 使用完成后返回信息
        """
        args = inspect.signature(goods.func).parameters  # type: ignore
        if goods.func:
            if args and list(args.keys())[0] != "kwargs":
                if asyncio.iscoroutinefunction(goods.func):
                    return await goods.func(
                        *cls.__parse_args(args, param, session, message, **kwargs)
                    )
                else:
                    return goods.func(
                        *cls.__parse_args(args, param, session, message, **kwargs)
                    )
            else:
                if asyncio.iscoroutinefunction(goods.func):
                    return await goods.func(
                        **kwargs,
                    )
                else:
                    return goods.func(**kwargs)

    @classmethod
    async def use(
        cls,
        bot: Bot,
        event: Event,
        session: EventSession,
        message: UniMsg,
        goods_name: str,
        num: int,
        text: str,
    ) -> str | MessageFactory | None:
        """使用道具

        参数:
            bot: Bot
            event: Event
            session: Session
            message: 消息
            goods_name: 商品名称
            num: 使用数量
            text: 其他信息

        返回:
            str | MessageFactory | None: 使用完成后返回信息
        """
        if goods_name.isdigit():
            user = await UserConsole.get_user(user_id=session.id1)  # type: ignore
            uuid = list(user.props.keys())[int(goods_name)]
            goods_info = await GoodsInfo.get_or_none(uuid=uuid)
        else:
            goods_info = await GoodsInfo.get_or_none(goods_name=goods_name)
        if not goods_info:
            return f"{goods_name} 不存在..."
        if goods_info.is_passive:
            return f"{goods_name} 是被动道具, 无法使用..."
        goods = cls.uuid2goods.get(goods_info.uuid)
        if not goods or not goods.func:
            return f"{goods_name} 未注册使用函数, 无法使用..."
        param, kwargs = cls.__build_params(
            bot, event, session, message, goods, num, text
        )
        if num > param.max_num_limit:
            return f"{goods_name} 单次使用最大数量为{param.max_num_limit}..."
        await cls.run_before_after(goods, param, "before", **kwargs)
        result = await cls.__run(goods, param, session, message, **kwargs)
        await cls.run_before_after(goods, param, "after", **kwargs)
        if not result and param.send_success_msg:
            result = f"使用道具 {goods.name} {num} 次成功！"
        return result

    @classmethod
    async def register_use(
        cls,
        name: str,
        uuid: str,
        func: Callable,
        send_success_msg: bool = True,
        max_num_limit: int = 1,
        before_handle: list[Callable] = [],
        after_handle: list[Callable] = [],
        **kwargs,
    ):
        """注册使用方法

        参数:
            uuid: uuid
            func: 使用函数
            send_success_msg: 使用成功时发送消息.
            max_num_limit: 单次最大使用限制.
            before_handle: 使用前函数.
            after_handle: 使用后函数.

        异常:
            ValueError: 该商品使用函数已被注册！
        """
        if uuid in cls.uuid2goods:
            raise ValueError("该商品使用函数已被注册！")
        kwargs["send_success_msg"] = send_success_msg
        kwargs["max_num_limit"] = max_num_limit
        cls.uuid2goods[uuid] = Goods(
            model=create_model(f"{uuid}_model", __base__=ShopParam, **kwargs),
            params=kwargs,
            before_handle=before_handle,
            after_handle=after_handle,
            name=name,
            func=func,
        )

    @classmethod
    async def buy_prop(
        cls, user_id: str, name: str, num: int = 1, platform: str | None = None
    ) -> str:
        """购买道具

        参数:
            user_id: 用户id
            name: 道具名称
            num: 购买数量.
            platform: 平台.

        返回:
            str: 返回小
        """
        if name == "神秘药水":
            return "你们看看就好啦，这是不可能卖给你们的~"
        if num < 0:
            return "购买的数量要大于0!"
        goods_list = await GoodsInfo.annotate().order_by("id").all()
        goods_list = [
            goods
            for goods in goods_list
            if goods.goods_limit_time > time.time() or goods.goods_limit_time == 0
        ]
        if name.isdigit():
            goods = goods_list[int(name) - 1]
        else:
            if filter_goods := [g for g in goods_list if g.goods_name == name]:
                goods = filter_goods[0]
            else:
                return "道具名称不存在..."
        user = await UserConsole.get_user(user_id, platform)
        price = goods.goods_price * num * goods.goods_discount
        if user.gold < price:
            return "糟糕! 您的金币好像不太够哦..."
        count = await UserPropsLog.filter(
            user_id=user_id, handle=PropHandle.BUY
        ).count()
        if goods.daily_limit and count >= goods.daily_limit:
            return "今天的购买已达限制了喔!"
        await UserGoldLog.create(user_id=user_id, gold=price, handle=GoldHandle.BUY)
        await UserPropsLog.create(
            user_id=user_id, uuid=goods.uuid, gold=price, num=num, handle=PropHandle.BUY
        )
        logger.info(
            f"花费 {price} 金币购买 {goods.goods_name} ×{num} 成功！",
            "购买道具",
            session=user_id,
        )
        user.gold -= int(price)
        if goods.uuid not in user.props:
            user.props[goods.uuid] = 0
        user.props[goods.uuid] += num
        await user.save(update_fields=["gold", "props"])
        return f"花费 {price} 金币购买 {goods.goods_name} ×{num} 成功！"

    @classmethod
    async def my_props(
        cls, user_id: str, name: str, platform: str | None = None
    ) -> BuildImage | None:
        """获取道具背包

        参数:
            user_id: 用户id
            name: 用户昵称
            platform: 平台.

        返回:
            BuildImage | None: 道具背包图片
        """
        user = await UserConsole.get_user(user_id, platform)
        if not user.props:
            return None
        result = await GoodsInfo.filter(uuid__in=user.props.keys()).all()
        data_list = []
        uuid2goods = {item.uuid: item for item in result}
        column_name = ["-", "使用ID", "名称", "数量", "简介"]
        for i, p in enumerate(user.props):
            prop = uuid2goods[p]
            data_list.append(
                [
                    (ICON_PATH / prop.icon, 33, 33) if prop.icon else "",
                    i,
                    prop.goods_name,
                    user.props[p],
                    prop.goods_description,
                ]
            )

        return await ImageTemplate.table_page(
            f"{name}的道具仓库", "", column_name, data_list
        )

    @classmethod
    async def my_cost(cls, user_id: str, platform: str | None = None) -> int:
        """用户金币

        参数:
            user_id: 用户id
            platform: 平台.

        返回:
            int: 金币数量
        """
        user = await UserConsole.get_user(user_id, platform)
        return user.gold

    @classmethod
    async def build_shop_image(cls) -> BuildImage:
        """制作商店图片

        返回:
            BuildImage: 商店图片
        """
        goods_lst = await GoodsInfo.get_all_goods()
        _dc = {}
        font_h = BuildImage.get_text_size("正")[1]
        h = 10
        _list: list[GoodsInfo] = []
        for goods in goods_lst:
            if goods.goods_limit_time == 0 or time.time() < goods.goods_limit_time:
                _list.append(goods)
        # A = BuildImage(1100, h, color="#f9f6f2")
        total_n = 0
        image_list = []
        for idx, goods in enumerate(_list):
            name_image = BuildImage(
                580, 40, font_size=25, color="#e67b6b", font="CJGaoDeGuo.otf"
            )
            await name_image.text(
                (15, 0), f"{idx + 1}.{goods.goods_name}", center_type="height"
            )
            await name_image.line((380, -5, 280, 45), "#a29ad6", 5)
            await name_image.text((390, 0), "售价：", center_type="height")
            if goods.goods_discount != 1:
                discount_price = int(goods.goods_discount * goods.goods_price)
                old_price_image = await BuildImage.build_text_image(
                    str(goods.goods_price), font_color=(194, 194, 194), size=15
                )
                await old_price_image.line(
                    (
                        0,
                        int(old_price_image.height / 2),
                        old_price_image.width + 1,
                        int(old_price_image.height / 2),
                    ),
                    (0, 0, 0),
                )
                await name_image.paste(old_price_image, (440, 0))
                await name_image.text((440, 15), str(discount_price), (255, 255, 255))
            else:
                await name_image.text(
                    (440, 0),
                    str(goods.goods_price),
                    (255, 255, 255),
                    center_type="height",
                )
            _tmp = await BuildImage.build_text_image(str(goods.goods_price), size=25)
            await name_image.text(
                (
                    440 + _tmp.width,
                    0,
                ),
                f" 金币",
                center_type="height",
            )
            des_image = None
            font_img = BuildImage(600, 80, font_size=20, color="#a29ad6")
            p = font_img.getsize("简介：")[0] + 20
            if goods.goods_description:
                des_list = goods.goods_description.split("\n")
                desc = ""
                for des in des_list:
                    if font_img.getsize(des)[0] > font_img.width - p - 20:
                        msg = ""
                        tmp = ""
                        for i in range(len(des)):
                            if font_img.getsize(tmp)[0] < font_img.width - p - 20:
                                tmp += des[i]
                            else:
                                msg += tmp + "\n"
                                tmp = des[i]
                        desc += msg
                        if tmp:
                            desc += tmp
                    else:
                        desc += des + "\n"
                if desc[-1] == "\n":
                    desc = desc[:-1]
                des_image = await text2image(desc, color="#a29ad6")
            goods_image = BuildImage(
                600,
                (50 + des_image.height) if des_image else 50,
                font_size=20,
                color="#a29ad6",
                font="CJGaoDeGuo.otf",
            )
            if des_image:
                await goods_image.text((15, 50), "简介：")
                await goods_image.paste(des_image, (p, 50))
            await name_image.circle_corner(5)
            await goods_image.paste(name_image, (0, 5), center_type="width")
            await goods_image.circle_corner(20)
            bk = BuildImage(
                1180,
                (50 + des_image.height) if des_image else 50,
                font_size=15,
                color="#f9f6f2",
                font="CJGaoDeGuo.otf",
            )
            if goods.icon and (ICON_PATH / goods.icon).exists():
                icon = BuildImage(70, 70, background=ICON_PATH / goods.icon)
                await bk.paste(icon)
            await bk.paste(goods_image, (70, 0))
            n = 0
            _w = 650
            # 添加限时图标和时间
            if goods.goods_limit_time > 0:
                n += 140
                _limit_time_logo = BuildImage(
                    40, 40, background=f"{IMAGE_PATH}/other/time.png"
                )
                await bk.paste(_limit_time_logo, (_w + 50, 0))
                _time_img = await BuildImage.build_text_image("限时！", size=23)
                await bk.paste(
                    _time_img,
                    (_w + 90, 10),
                )
                limit_time = time.strftime(
                    "%Y-%m-%d %H:%M", time.localtime(goods.goods_limit_time)
                ).split()
                y_m_d = limit_time[0]
                _h_m = limit_time[1].split(":")
                h_m = _h_m[0] + "时 " + _h_m[1] + "分"
                await bk.text((_w + 55, 38), str(y_m_d))
                await bk.text((_w + 65, 57), str(h_m))
                _w += 140
            if goods.goods_discount != 1:
                n += 140
                _discount_logo = BuildImage(
                    30, 30, background=f"{IMAGE_PATH}/other/discount.png"
                )
                await bk.paste(_discount_logo, (_w + 50, 10))
                _tmp = await BuildImage.build_text_image("折扣！", size=23)
                await bk.paste(_tmp, (_w + 90, 15))
                _tmp = await BuildImage.build_text_image(
                    f"{10 * goods.goods_discount:.1f} 折",
                    size=30,
                    font_color=(85, 156, 75),
                )
                await bk.paste(_tmp, (_w + 50, 44))
                _w += 140
            if goods.daily_limit != 0:
                n += 140
                _daily_limit_logo = BuildImage(
                    35, 35, background=f"{IMAGE_PATH}/other/daily_limit.png"
                )
                await bk.paste(_daily_limit_logo, (_w + 50, 10))
                _tmp = await BuildImage.build_text_image(
                    "限购！",
                    size=23,
                )
                await bk.paste(_tmp, (_w + 90, 20))
                _tmp = await BuildImage.build_text_image(
                    f"{goods.daily_limit}", size=30
                )
                await bk.paste(_tmp, (_w + 72, 45))
            if total_n < n:
                total_n = n
            if n:
                await bk.line((650, -1, 650 + n, -1), "#a29ad6", 5)
                # await bk.aline((650, 80, 650 + n, 80), "#a29ad6", 5)

            # 添加限时图标和时间
            image_list.append(bk)
            # await A.apaste(bk, (0, current_h), True)
            # current_h += 90
        h = 0
        current_h = 0
        for img in image_list:
            h += img.height + 10
        A = BuildImage(1100, h, color="#f9f6f2")
        for img in image_list:
            await A.paste(img, (0, current_h))
            current_h += img.height + 10
        w = 950
        if total_n:
            w += total_n
        h = A.height + 230 + 100
        h = 1000 if h < 1000 else h
        shop_logo = BuildImage(100, 100, background=f"{IMAGE_PATH}/other/shop_text.png")
        shop = BuildImage(w, h, font_size=20, color="#f9f6f2")
        await shop.paste(A, (20, 230))
        await shop.paste(shop_logo, (450, 30))
        await shop.text(
            (
                int((1000 - shop.getsize("注【通过 序号 或者 商品名称 购买】")[0]) / 2),
                170,
            ),
            "注【通过 序号 或者 商品名称 购买】",
        )
        await shop.text(
            (20, h - 100),
            "神秘药水\t\t售价：9999999金币\n\t\t鬼知道会有什么效果~",
        )
        return shop
