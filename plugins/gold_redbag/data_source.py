import os
import random
from io import BytesIO
from typing import Tuple, Union

from nonebot.adapters.onebot.v11 import Bot

from configs.config import NICKNAME, Config
from configs.path_config import IMAGE_PATH
from models.bag_user import BagUser
from utils.image_utils import BuildImage
from utils.message_builder import image
from utils.utils import get_user_avatar, is_number

from .config import FESTIVE_KEY, GroupRedBag, RedBag


async def end_festive_red_bag(bot: Bot, group_red_bag: GroupRedBag):
    """结算节日红包

    参数:
        bot: Bot
        group_red_bag: GroupRedBag
    """
    if festive_red_bag := group_red_bag.festive_red_bag_expire():
        rank_num = Config.get_config("gold_redbag", "RANK_NUM") or 10
        rank_image = await festive_red_bag.build_amount_rank(rank_num)
        message = (
            f"{NICKNAME}的节日红包过时了，一共开启了 "
            f"{len(festive_red_bag.open_user)}"
            f" 个红包，共 {sum(festive_red_bag.open_user.values())} 金币\n" + image(rank_image)
        )
        await bot.send_group_msg(group_id=int(group_red_bag.group_id), message=message)


async def check_gold(
    user_id: str, group_id: str, amount: Union[str, int]
) -> Tuple[bool, str]:
    """检查金币数量是否合法

    参数:
        user_id: 用户id
        group_id: 群聊id
        amount: 金币数量

    返回:
        Tuple[bool, str]: 是否合法以及提示语
    """
    if is_number(amount):
        amount = int(amount)
        user_gold = await BagUser.get_gold(user_id, group_id)
        if amount < 1:
            return False, "小气鬼，要别人倒贴金币给你嘛！"
        if user_gold < amount:
            return False, "没有金币的话请不要发红包..."
        return True, ""
    else:
        return False, "给我好好的输入红包里金币的数量啊喂！"


async def random_red_bag_background(
    user_id: Union[str, int], msg="恭喜发财 大吉大利"
) -> BuildImage:
    """构造发送红包图片

    参数:
        user_id: 用户id
        msg: 红包消息.

    异常:
        ValueError: 图片背景列表为空

    返回:
        BuildImage: 构造后的图片
    """
    background_list = os.listdir(f"{IMAGE_PATH}/prts/redbag_2")
    if not background_list:
        raise ValueError("prts/redbag_1 背景图列表为空...")
    random_redbag = random.choice(background_list)
    redbag = BuildImage(
        0, 0, font_size=38, background=IMAGE_PATH / "prts" / "redbag_2" / random_redbag
    )
    ava_byte = await get_user_avatar(user_id)
    ava = None
    if ava_byte:
        ava = BuildImage(65, 65, background=BytesIO(ava_byte))
    else:
        ava = BuildImage(65, 65, color=(0, 0, 0), is_alpha=True)
    await ava.acircle()
    await redbag.atext(
        (int((redbag.size[0] - redbag.getsize(msg)[0]) / 2), 210), msg, (240, 218, 164)
    )
    await redbag.apaste(ava, (int((redbag.size[0] - ava.size[0]) / 2), 130), True)
    return redbag


async def build_open_result_image(
    red_bag: RedBag, user_id: Union[int, str], amount: int
) -> BuildImage:
    """构造红包开启图片

    参数:
        red_bag: RedBag
        user_id: 开启红包用户id
        amount: 开启红包获取的金额

    异常:
        ValueError: 图片背景列表为空

    返回:
        BuildImage: 构造后的图片
    """
    background_list = os.listdir(f"{IMAGE_PATH}/prts/redbag_1")
    if not background_list:
        raise ValueError("prts/redbag_1 背景图列表为空...")
    random_redbag = random.choice(background_list)
    head = BuildImage(
        1000,
        980,
        font_size=30,
        background=IMAGE_PATH / "prts" / "redbag_1" / random_redbag,
    )
    size = BuildImage(0, 0, font_size=50).getsize(red_bag.name)
    ava_bk = BuildImage(100 + size[0], 66, is_alpha=True, font_size=50)

    ava_byte = await get_user_avatar(user_id)
    ava = None
    if ava_byte:
        ava = BuildImage(66, 66, is_alpha=True, background=BytesIO(ava_byte))
    else:
        ava = BuildImage(66, 66, color=(0, 0, 0), is_alpha=True)
    await ava_bk.apaste(ava)
    ava_bk.text((100, 7), red_bag.name)
    ava_bk_w, ava_bk_h = ava_bk.size
    await head.apaste(ava_bk, (int((1000 - ava_bk_w) / 2), 300), alpha=True)
    size = BuildImage(0, 0, font_size=150).getsize(amount)
    amount_image = BuildImage(size[0], size[1], is_alpha=True, font_size=150)
    await amount_image.atext((0, 0), str(amount), fill=(209, 171, 108))
    # 金币中文
    await head.apaste(amount_image, (int((1000 - size[0]) / 2) - 50, 460), alpha=True)
    await head.atext(
        (int((1000 - size[0]) / 2 + size[0]) - 50, 500 + size[1] - 70),
        "金币",
        fill=(209, 171, 108),
    )
    # 剩余数量和金额
    text = (
        f"已领取"
        f"{red_bag.num - len(red_bag.open_user)}"
        f"/{red_bag.num}个，"
        f"共{sum(red_bag.open_user.values())}/{red_bag.amount}金币"
    )
    await head.atext((350, 900), text, (198, 198, 198))
    return head
