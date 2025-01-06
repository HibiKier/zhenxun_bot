from zhenxun.models.user_console import UserConsole
from zhenxun.utils.decorator.shop import shop_register


@shop_register(
    name="神秘药水",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="小秘密",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    await UserConsole.add_gold(
        user_id,
        1000000,
        "shop",
    )
    return "使用道具神秘药水成功！你滴金币+1000000！"


@shop_register(
    name="测试道具A1",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A2",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A3",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A4",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A5",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A6",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A7",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A8",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A9",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A10",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A11",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A12",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass


@shop_register(
    name="测试道具A13",
    price=999999,
    des="鬼知道会有什么效果，要不试试？",
    partition="TEST",
    icon="mysterious_potion.png",
)
async def _(user_id: str):
    pass
