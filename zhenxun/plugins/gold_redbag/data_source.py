import asyncio
import os
import random
from io import BytesIO
from typing import Dict

from nonebot.adapters import Bot
from nonebot.exception import ActionFailed
from nonebot_plugin_alconna import UniMessage

from zhenxun.configs.config import BotConfig, Config
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.models.user_console import UserConsole
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

from .config import FestiveRedBagManage, GroupRedBag, RedBag


class RedBagManager:

    _data: Dict[str, GroupRedBag] = {}

    @classmethod
    def get_group_data(cls, group_id: str) -> GroupRedBag:
        """获取群组红包数据

        参数:
            group_id: 群组id

        返回:
            GroupRedBag | None: GroupRedBag
        """
        if group_id not in cls._data:
            cls._data[group_id] = GroupRedBag(group_id)
        return cls._data[group_id]

    @classmethod
    async def _auto_end_festive_red_bag(cls, bot: Bot, group_id: str, platform: str):
        """自动结算节日红包

        参数:
            bot: Bot
            group_id: 群组id
            platform: 平台
        """
        if target := PlatformUtils.get_target(bot, group_id=group_id):
            rank_num = Config.get_config("gold_redbag", "RANK_NUM") or 10
            group_red_bag = cls.get_group_data(group_id)
            red_bag = group_red_bag.get_festive_red_bag()
            if not red_bag:
                return
            rank_image = await red_bag.build_amount_rank(rank_num, platform)
            if red_bag.is_festival and red_bag.uuid:
                FestiveRedBagManage.remove(red_bag.uuid)
            await asyncio.sleep(random.randint(1, 5))
            try:
                await MessageUtils.build_message(
                    [
                        f"{BotConfig.self_nickname}的节日红包过时了，一共开启了 "
                        f"{len(red_bag.open_user)}"
                        f" 个红包，共 {sum(red_bag.open_user.values())} 金币\n",
                        rank_image,
                    ]
                ).send(target=target, bot=bot)
            except ActionFailed:
                pass

    @classmethod
    async def end_red_bag(
        cls,
        group_id: str,
        user_id: str | None = None,
        is_festive: bool = False,
        platform: str = "",
    ) -> UniMessage | None:
        """结算红包

        参数:
            group_id: 群组id或频道id
            user_id: 用户id
            is_festive: 是否节日红包
            platform: 用户平台
        """
        rank_num = Config.get_config("gold_redbag", "RANK_NUM") or 10
        group_red_bag = cls.get_group_data(group_id)
        if not group_red_bag:
            return None
        if is_festive:
            if festive_red_bag := group_red_bag.festive_red_bag_expire():
                rank_image = await festive_red_bag.build_amount_rank(rank_num, platform)
                return MessageUtils.build_message(
                    [
                        f"{BotConfig.self_nickname}的节日红包过时了，一共开启了 "
                        f"{len(festive_red_bag.open_user)}"
                        f" 个红包，共 {sum(festive_red_bag.open_user.values())} 金币\n",
                        rank_image,
                    ]
                )
        else:
            if not user_id:
                return None
            return_gold, red_bag = await group_red_bag.settlement(user_id, platform)
            if red_bag:
                rank_image = await red_bag.build_amount_rank(rank_num, platform)
                return MessageUtils.build_message(
                    [
                        f"已成功退还了 " f"{return_gold} 金币\n",
                        rank_image.pic2bytes(),
                    ]
                )

    @classmethod
    async def check_gold(cls, user_id: str, amount: int, platform: str) -> str | None:
        """检查金币数量是否合法

        参数:
            user_id: 用户id
            amount: 金币数量
            platform: 所属平台

        返回:
            tuple[bool, str]: 是否合法以及提示语
        """
        user = await UserConsole.get_user(user_id, platform)
        if amount < 1:
            return "小气鬼，要别人倒贴金币给你嘛！"
        if user.gold < amount:
            return "没有金币的话请不要发红包..."
        return None

    @classmethod
    async def random_red_bag_background(
        cls, user_id: str, msg: str = "恭喜发财 大吉大利", platform: str = ""
    ) -> BuildImage:
        """构造发送红包图片

        参数:
            user_id: 用户id
            msg: 红包消息.
            platform: 平台.

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
            0,
            0,
            font_size=38,
            background=IMAGE_PATH / "prts" / "redbag_2" / random_redbag,
        )
        ava_byte = await PlatformUtils.get_user_avatar(user_id, platform)
        ava = None
        if ava_byte:
            ava = BuildImage(65, 65, background=BytesIO(ava_byte))
        else:
            ava = BuildImage(65, 65, color=(0, 0, 0))
        await ava.circle()
        await redbag.text(
            (int((redbag.size[0] - redbag.getsize(msg)[0]) / 2), 210),
            msg,
            (240, 218, 164),
        )
        await redbag.paste(ava, (int((redbag.size[0] - ava.size[0]) / 2), 130))
        return redbag

    @classmethod
    async def build_open_result_image(
        cls, red_bag: RedBag, user_id: str, amount: int, platform: str
    ) -> BuildImage:
        """构造红包开启图片

        参数:
            red_bag: RedBag
            user_id: 开启红包用户id
            amount: 开启红包获取的金额
            platform: 平台

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
        size = BuildImage.get_text_size(red_bag.name, font_size=50)
        ava_bk = BuildImage(100 + size[0], 66, (255, 255, 255, 0), font_size=50)

        ava_byte = await PlatformUtils.get_user_avatar(user_id, platform)
        ava = None
        if ava_byte:
            ava = BuildImage(66, 66, background=BytesIO(ava_byte))
        else:
            ava = BuildImage(66, 66, color=(0, 0, 0))
        await ava_bk.paste(ava)
        await ava_bk.text((100, 7), red_bag.name)
        ava_bk_w, ava_bk_h = ava_bk.size
        await head.paste(ava_bk, (int((1000 - ava_bk_w) / 2), 300))
        size = BuildImage.get_text_size(str(amount), font_size=150)
        amount_image = BuildImage(size[0], size[1], (255, 255, 255, 0), font_size=150)
        await amount_image.text((0, 0), str(amount), fill=(209, 171, 108))
        # 金币中文
        await head.paste(amount_image, (int((1000 - size[0]) / 2) - 50, 460))
        await head.text(
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
        await head.text((350, 900), text, (198, 198, 198))
        return head
