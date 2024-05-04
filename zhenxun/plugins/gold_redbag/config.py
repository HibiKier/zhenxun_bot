import random
import time
from io import BytesIO
from typing import Dict

from pydantic import BaseModel

from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.models.user_console import UserConsole
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.platform import PlatformUtils
from zhenxun.utils.utils import get_user_avatar

from .model import RedbagUser

FESTIVE_KEY = "FESTIVE"
"""节日红包KEY"""


class FestiveRedBagManage:

    _data: Dict[str, list[str]] = {}

    @classmethod
    def add(cls, uuid: str):
        cls._data[uuid] = []

    @classmethod
    def open(cls, uuid: str, uid: str):
        if uuid in cls._data and uid not in cls._data[uuid]:
            cls._data[uuid].append(uid)

    @classmethod
    def remove(cls, uuid: str):
        if uuid in cls._data:
            del cls._data[uuid]

    @classmethod
    def check(cls, uuid: str, uid: str):
        if uuid in cls._data:
            return uid not in cls._data[uuid]
        return False


class RedBag(BaseModel):
    """
    红包
    """

    group_id: str
    """所属群聊"""
    name: str
    """红包名称"""
    amount: int
    """总金币"""
    num: int
    """红包数量"""
    promoter: str
    """发起人昵称"""
    promoter_id: str
    """发起人id"""
    is_festival: bool
    """是否为节日红包"""
    timeout: int
    """过期时间"""
    assigner: str | None = None
    """指定人id"""
    start_time: float
    """红包发起时间"""
    open_user: Dict[str, int] = {}
    """开启用户"""
    red_bag_list: list[int]
    """红包金额列表"""
    uuid: str | None
    """uuid"""

    async def build_amount_rank(self, num: int, platform: str) -> BuildImage:
        """生成结算红包图片

        参数:
            num: 查看的排名数量.
            platform: 平台.

        返回:
            BuildImage: 结算红包图片
        """
        user_image_list = []
        if self.open_user:
            sort_data = sorted(
                self.open_user.items(), key=lambda item: item[1], reverse=True
            )
            num = num if num < len(self.open_user) else len(self.open_user)
            user_id_list = [sort_data[i][0] for i in range(num)]
            group_user_list = await GroupInfoUser.filter(
                group_id=self.group_id, user_id__in=user_id_list
            ).all()
            for i in range(num):
                user_background = BuildImage(600, 100, font_size=30)
                user_id, amount = sort_data[i]
                user_ava_bytes = await PlatformUtils.get_user_avatar(user_id, platform)
                user_ava = None
                if user_ava_bytes:
                    user_ava = BuildImage(80, 80, background=BytesIO(user_ava_bytes))
                else:
                    user_ava = BuildImage(80, 80)
                await user_ava.circle_corner(10)
                await user_background.paste(user_ava, (130, 10))
                no_image = BuildImage(100, 100, font_size=65, font="CJGaoDeGuo.otf")
                await no_image.text((0, 0), f"{i+1}", center_type="center")
                await no_image.line((99, 10, 99, 90), "#b9b9b9")
                await user_background.paste(no_image)
                name = [
                    user.user_name
                    for user in group_user_list
                    if user_id == user.user_id
                ]
                await user_background.text((225, 15), name[0] if name else "")
                amount_image = await BuildImage.build_text_image(
                    f"{amount} 元", size=30, font_color="#cdac72"
                )
                await user_background.paste(
                    amount_image, (user_background.width - amount_image.width - 20, 50)
                )
                await user_background.line((225, 99, 590, 99), "#b9b9b9")
                user_image_list.append(user_background)
        background = BuildImage(600, 150 + len(user_image_list) * 100)
        top = BuildImage(600, 100, color="#f55545", font_size=30)
        promoter_ava_bytes = await PlatformUtils.get_user_avatar(
            self.promoter_id, platform
        )
        promoter_ava = None
        if promoter_ava_bytes:
            promoter_ava = BuildImage(60, 60, background=BytesIO(promoter_ava_bytes))
        else:
            promoter_ava = BuildImage(60, 60)
        await promoter_ava.circle()
        await top.paste(promoter_ava, (10, 0), "height")
        await top.text((80, 33), self.name, (255, 255, 255))
        right_text = BuildImage(150, 100, color="#f55545", font_size=30)
        await right_text.text((10, 33), "结算排行", (255, 255, 255))
        await right_text.line((4, 10, 4, 90), (255, 255, 255), 2)
        await top.paste(right_text, (460, 0))
        await background.paste(top)
        cur_h = 110
        for user_image in user_image_list:
            await background.paste(user_image, (0, cur_h))
            cur_h += user_image.height
        return background


class GroupRedBag:
    """
    群组红包管理
    """

    def __init__(self, group_id: str):
        self.group_id = group_id
        self._data: Dict[str, RedBag] = {}
        """红包列表"""

    def remove_festive_red_bag(self):
        """删除节日红包"""
        _key = None
        for k, red_bag in self._data.items():
            if red_bag.is_festival:
                _key = k
                break
        if _key:
            del self._data[_key]

    def get_festive_red_bag(self) -> RedBag | None:
        """获取节日红包

        返回:
            RedBag | None: 节日红包
        """
        for _, red_bag in self._data.items():
            if red_bag.is_festival:
                return red_bag
        return None

    def get_user_red_bag(self, user_id: str) -> RedBag | None:
        """获取用户塞红包数据

        参数:
            user_id: 用户id

        返回:
            RedBag | None: RedBag
        """
        return self._data.get(str(user_id))

    def check_open(self, user_id: str) -> bool:
        """检查是否有可开启的红包

        参数:
            user_id: 用户id

        返回:
            bool: 是否有可开启的红包
        """
        user_id = str(user_id)
        for _, red_bag in self._data.items():
            if red_bag.assigner:
                if red_bag.assigner == user_id:
                    return True
            else:
                if user_id not in red_bag.open_user:
                    return True
        return False

    def check_timeout(self, user_id: str) -> int:
        """判断用户红包是否过期

        参数:
            user_id: 用户id

        返回:
            int: 距离过期时间
        """
        if user_id in self._data:
            reg_bag = self._data[user_id]
            now = time.time()
            if now < reg_bag.timeout + reg_bag.start_time:
                return int(reg_bag.timeout + reg_bag.start_time - now)
        return -1

    async def open(
        self, user_id: str, platform: str | None = None
    ) -> tuple[Dict[str, tuple[int, RedBag]], list[RedBag]]:
        """开启红包

        参数:
            user_id: 用户id
            platform: 所属平台

        返回:
            Dict[str, tuple[int, RedBag]]: 键为发起者id, 值为开启金额以及对应RedBag
            list[RedBag]: 开完的红包
        """
        open_data = {}
        settlement_list: list[RedBag] = []
        for _, red_bag in self._data.items():
            if red_bag.num > len(red_bag.open_user):
                if red_bag.is_festival and red_bag.uuid:
                    if not FestiveRedBagManage.check(red_bag.uuid, user_id):
                        continue
                    FestiveRedBagManage.open(red_bag.uuid, user_id)
                is_open = False
                if red_bag.assigner:
                    is_open = red_bag.assigner == user_id
                else:
                    is_open = user_id not in red_bag.open_user
                if is_open:
                    random_amount = red_bag.red_bag_list.pop()
                    await RedbagUser.add_redbag_data(
                        user_id, self.group_id, "get", random_amount
                    )
                    await UserConsole.add_gold(
                        user_id, random_amount, "gold_redbag", platform
                    )
                    red_bag.open_user[user_id] = random_amount
                    open_data[red_bag.promoter_id] = (random_amount, red_bag)
                    if red_bag.num == len(red_bag.open_user):
                        # 红包开完，结算
                        settlement_list.append(red_bag)
        if settlement_list:
            for uid in [red_bag.promoter_id for red_bag in settlement_list]:
                if uid in self._data:
                    del self._data[uid]
        return open_data, settlement_list

    def festive_red_bag_expire(self) -> RedBag | None:
        """节日红包过期

        返回:
            RedBag | None: 过期的节日红包
        """
        if FESTIVE_KEY in self._data:
            red_bag = self._data[FESTIVE_KEY]
            del self._data[FESTIVE_KEY]
            return red_bag
        return None

    async def settlement(
        self, user_id: str, platform: str | None = None
    ) -> tuple[int | None, RedBag | None]:
        """红包退回

        参数:
            user_id: 用户id, 指定id时结算指定用户红包.
            platform: 用户平台

        返回:
            tuple[int | None, RedBag | None]: 退回金币, 红包
        """
        if red_bag := self._data.get(user_id):
            del self._data[user_id]
            if red_bag.is_festival and red_bag.uuid:
                FestiveRedBagManage.remove(red_bag.uuid)
            if red_bag.red_bag_list:
                """退还剩余金币"""
                if amount := sum(red_bag.red_bag_list):
                    await UserConsole.add_gold(user_id, amount, "gold_redbag", platform)
                    return amount, red_bag
        return None, None

    async def add_red_bag(
        self,
        name: str,
        amount: int,
        num: int,
        promoter: str,
        promoter_id: str,
        festival_uuid: str | None = None,
        timeout: int = 60,
        assigner: str | None = None,
        platform: str | None = None,
    ):
        """添加红包

        参数:
            name: 红包名称
            amount: 金币数量
            num: 红包数量
            promoter: 发起人昵称
            promoter_id: 发起人id
            festival_uuid: 节日红包uuid.
            timeout: 超时时间.
            assigner: 指定人.
            platform: 用户平台.
        """
        user = await UserConsole.get_user(promoter_id, platform)
        if not festival_uuid and (amount < 1 or user.gold < amount):
            raise ValueError("红包金币不足或用户金币不足")
        red_bag_list = self._random_red_bag(amount, num)
        if not festival_uuid:
            user.gold -= amount
            await RedbagUser.add_redbag_data(promoter_id, self.group_id, "send", amount)
            await user.save(update_fields=["gold"])
        self._data[promoter_id] = RedBag(
            group_id=self.group_id,
            name=name,
            amount=amount,
            num=num,
            promoter=promoter,
            promoter_id=promoter_id,
            is_festival=bool(festival_uuid),
            timeout=timeout,
            start_time=time.time(),
            assigner=assigner,
            red_bag_list=red_bag_list,
            uuid=festival_uuid,
        )

    def _random_red_bag(self, amount: int, num: int) -> list[int]:
        """初始化红包金币

        参数:
            amount: 金币数量
            num: 红包数量

        返回:
            list[int]: 红包列表
        """
        red_bag_list = []
        for _ in range(num - 1):
            tmp = int(amount / random.choice(range(3, num + 3)))
            red_bag_list.append(tmp)
            amount -= tmp
        red_bag_list.append(amount)
        return red_bag_list
