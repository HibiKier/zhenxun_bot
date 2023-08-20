import random
import time
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union, overload

from pydantic import BaseModel

from models.bag_user import BagUser
from models.group_member_info import GroupInfoUser
from plugins.gold_redbag.model import RedbagUser
from utils.image_utils import BuildImage
from utils.utils import get_user_avatar

FESTIVE_KEY = "FESTIVE"
"""节日红包KEY"""


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
    assigner: Optional[str] = None
    """指定人id"""
    start_time: float
    """红包发起时间"""
    open_user: Dict[str, int] = {}
    """开启用户"""
    red_bag_list: List[int]

    async def build_amount_rank(self, num: int = 10) -> BuildImage:
        """生成结算红包图片

        参数:
            num: 查看的排名数量.

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
                user_ava_bytes = await get_user_avatar(user_id)
                user_ava = None
                if user_ava_bytes:
                    user_ava = BuildImage(80, 80, background=BytesIO(user_ava_bytes))
                else:
                    user_ava = BuildImage(80, 80)
                await user_ava.acircle_corner(10)
                await user_background.apaste(user_ava, (130, 10), True)
                no_image = BuildImage(100, 100, font_size=65, font="CJGaoDeGuo.otf")
                await no_image.atext((0, 0), f"{i+1}", center_type="center")
                await no_image.aline((99, 10, 99, 90), "#b9b9b9")
                await user_background.apaste(no_image)
                name = [
                    user.user_name
                    for user in group_user_list
                    if user_id == user.user_id
                ]
                await user_background.atext((225, 15), name[0] if name else "")
                amount_image = BuildImage(
                    0, 0, plain_text=f"{amount} 元", font_size=30, font_color="#cdac72"
                )
                await user_background.apaste(
                    amount_image, (user_background.w - amount_image.w - 20, 50), True
                )
                await user_background.aline((225, 99, 590, 99), "#b9b9b9")
                user_image_list.append(user_background)
        background = BuildImage(600, 150 + len(user_image_list) * 100)
        top = BuildImage(600, 100, color="#f55545", font_size=30)
        promoter_ava_bytes = await get_user_avatar(self.promoter_id)
        promoter_ava = None
        if promoter_ava_bytes:
            promoter_ava = BuildImage(60, 60, background=BytesIO(promoter_ava_bytes))
        else:
            promoter_ava = BuildImage(60, 60)
        await promoter_ava.acircle()
        await top.apaste(promoter_ava, (10, 0), True, "by_height")
        await top.atext((80, 33), self.name, (255, 255, 255))
        right_text = BuildImage(150, 100, color="#f55545", font_size=30)
        await right_text.atext((10, 33), "结算排行", (255, 255, 255))
        await right_text.aline((4, 10, 4, 90), (255, 255, 255), 2)
        await top.apaste(right_text, (460, 0))
        await background.apaste(top)
        cur_h = 110
        for user_image in user_image_list:
            await background.apaste(user_image, (0, cur_h))
            cur_h += user_image.h
        return background


class GroupRedBag:

    """
    群组红包管理
    """

    def __init__(self, group_id: Union[int, str]):
        self.group_id = str(group_id)
        self._data: Dict[str, RedBag] = {}
        """红包列表"""

    def get_user_red_bag(self, user_id: Union[str, int]) -> Optional[RedBag]:
        """获取用户塞红包数据

        参数:
            user_id: 用户id

        返回:
            Optional[RedBag]: RedBag
        """
        return self._data.get(str(user_id))

    def check_open(self, user_id: Union[str, int]) -> bool:
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

    def check_timeout(self, user_id: Union[int, str]) -> int:
        """判断用户红包是否过期

        参数:
            user_id: 用户id

        返回:
            int: 距离过期时间
        """
        user_id = str(user_id)
        if user_id in self._data:
            reg_bag = self._data[user_id]
            now = time.time()
            if now < reg_bag.timeout + reg_bag.start_time:
                return int(reg_bag.timeout + reg_bag.start_time - now)
        return -1

    async def open(
        self, user_id: Union[int, str]
    ) -> Tuple[Dict[str, Tuple[int, RedBag]], List[RedBag]]:
        """开启红包

        参数:
            user_id: 用户id

        返回:
            Dict[str, Tuple[int, RedBag]]: 键为发起者id, 值为开启金额以及对应RedBag
            List[RedBag]: 开完的红包
        """
        user_id = str(user_id)
        open_data = {}
        settlement_list: List[RedBag] = []
        for _, red_bag in self._data.items():
            if red_bag.num > len(red_bag.open_user):
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
                    await BagUser.add_gold(user_id, self.group_id, random_amount)
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

    def festive_red_bag_expire(self) -> Optional[RedBag]:
        """节日红包过期

        返回:
            Optional[RedBag]: 过期的节日红包
        """
        if FESTIVE_KEY in self._data:
            red_bag = self._data[FESTIVE_KEY]
            del self._data[FESTIVE_KEY]
            return red_bag
        return None

    async def settlement(
        self, user_id: Optional[Union[int, str]] = None
    ) -> Optional[int]:
        """红包退回

        参数:
            user_id: 用户id, 指定id时结算指定用户红包.

        返回:
            int: 退回金币
        """
        user_id = str(user_id)
        if user_id:
            if red_bag := self._data.get(user_id):
                del self._data[user_id]
                if red_bag.red_bag_list:
                    # 退还剩余金币
                    if amount := sum(red_bag.red_bag_list):
                        await BagUser.add_gold(user_id, self.group_id, amount)
                        return amount
        return None

    async def add_red_bag(
        self,
        name: str,
        amount: int,
        num: int,
        promoter: str,
        promoter_id: str,
        is_festival: bool = False,
        timeout: int = 60,
        assigner: Optional[str] = None,
    ):
        """添加红包

        参数:
            name: 红包名称
            amount: 金币数量
            num: 红包数量
            promoter: 发起人昵称
            promoter_id: 发起人id
            is_festival: 是否为节日红包.
            timeout: 超时时间.
            assigner: 指定人.
        """
        user_gold = await BagUser.get_gold(promoter_id, self.group_id)
        if not is_festival and (amount < 1 or user_gold < amount):
            raise ValueError("红包金币不足或用户金币不足")
        red_bag_list = self._random_red_bag(amount, num)
        if not is_festival:
            await BagUser.spend_gold(promoter_id, self.group_id, amount)
            await RedbagUser.add_redbag_data(promoter_id, self.group_id, "send", amount)
        self._data[promoter_id] = RedBag(
            group_id=self.group_id,
            name=name,
            amount=amount,
            num=num,
            promoter=promoter,
            promoter_id=promoter_id,
            is_festival=is_festival,
            timeout=timeout,
            start_time=time.time(),
            assigner=assigner,
            red_bag_list=red_bag_list,
        )

    def _random_red_bag(self, amount: int, num: int) -> List[int]:
        """初始化红包金币

        参数:
            amount: 金币数量
            num: 红包数量

        返回:
            List[int]: 红包列表
        """
        red_bag_list = []
        for _ in range(num - 1):
            tmp = int(amount / random.choice(range(3, num + 3)))
            red_bag_list.append(tmp)
            amount -= tmp
        red_bag_list.append(amount)
        return red_bag_list
