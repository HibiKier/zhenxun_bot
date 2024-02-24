from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Subcommand, on_alconna
from nonebot_plugin_saa import Image, Text
from nonebot_plugin_session import EventSession
from nonebot_plugin_userinfo import EventUserInfo, UserInfo

from zhenxun.configs.utils import BaseBlock, PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import BlockType, PluginType

from ._data_source import ShopManage

__plugin_meta__ = PluginMetadata(
    name="商店",
    description="商店系统[金币回收计划]",
    usage="""
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
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.NORMAL,
        menu_type="商店",
        limits=[BaseBlock(check_type=BlockType.GROUP)],
    ).dict(),
)

# TODO: 修改操作，shortcut

_matcher = on_alconna(
    Alconna(
        "shop",
        Subcommand("my-cost", help_text="我的金币"),
        Subcommand("my-props", help_text="我的道具"),
        Subcommand("buy", Args["name", str]["num", int, 1], help_text="购买道具"),
        Subcommand("use", Args["name", str]["num?", int, 1], help_text="使用道具"),
    ),
    priority=5,
    block=True,
)


@_matcher.assign("$main")
async def _(session: EventSession, arparma: Arparma):
    image = await ShopManage.build_shop_image()
    logger.info("查看商店", arparma.header_result, session=session)
    await Image(image.pic2bs4()).send()


@_matcher.assign("my-cost")
async def _(session: EventSession, arparma: Arparma):
    if session.id1:
        logger.info("查看金币", arparma.header_result, session=session)
        gold = await ShopManage.my_cost(session.id1, session.platform)
        await Text(f"你的当前余额: {gold}").send(reply=True)
    else:
        await Text(f"用户id为空...").send(reply=True)


@_matcher.assign("my-props")
async def _(
    session: EventSession, arparma: Arparma, user_info: UserInfo = EventUserInfo()
):
    if session.id1:
        logger.info("查看道具", arparma.header_result, session=session)
        if image := await ShopManage.my_props(
            session.id1,
            user_info.user_displayname or user_info.user_name,
            session.platform,
        ):
            await Image(image.pic2bs4()).finish(reply=True)
        return await Text(f"你的道具为空捏...").send(reply=True)
    else:
        await Text(f"用户id为空...").send(reply=True)


@_matcher.assign("buy")
async def _(session: EventSession, arparma: Arparma, name: str, num: int):
    if session.id1:
        logger.info(
            f"购买道具 {name}, 数量: {num}",
            arparma.header_result,
            session=session,
        )
        result = await ShopManage.buy_prop(session.id1, name, num, session.platform)
        await Text(result).send(reply=True)
    else:
        await Text(f"用户id为空...").send(reply=True)


@_matcher.assign("use")
async def _(session: EventSession, arparma: Arparma, name: str, num: int):
    pass
