from utils.manager.data_class import StaticData
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.exception import ActionFailed
from services.log import logger
from typing import Optional
from utils.image_utils import BuildImage
from utils.utils import get_user_avatar
from pathlib import Path
from io import BytesIO


class RequestManager(StaticData):

    """
    好友请求/邀请请求 管理
    """

    def __init__(self, file: Optional[Path]):
        super().__init__(file)
        if not self._data:
            self._data = {"private": {}, "group": {}}

    def add_request(
        self,
        id_: int,
        type_: str,
        flag: str,
        *,
        nickname: Optional[str] = None,
        level: Optional[int] = None,
        sex: Optional[str] = None,
        age: Optional[str] = None,
        from_: Optional[str] = "",
        comment: Optional[str] = None,
        invite_group: Optional[int] = None,
        group_name: Optional[str] = None,
    ):
        """
        添加一个请求
        :param id_: id，用户id或群id
        :param type_: 类型，private 或 group
        :param flag: event.flag
        :param nickname: 用户昵称
        :param level: 等级
        :param sex: 性别
        :param age: 年龄
        :param from_: 请求来自
        :param comment: 附加消息
        :param invite_group: 邀请群聊
        :param group_name: 群聊名称
        """
        self._data[type_][str(len(self._data[type_].keys()))] = {
            "id": id_,
            "flag": flag,
            "nickname": nickname,
            "level": level,
            "sex": sex,
            "age": age,
            "from": from_,
            "comment": comment,
            "invite_group": invite_group,
            "group_name": group_name,
        }
        self.save()

    def remove_request(self, type_: str, id_: int):
        """
        删除一个请求数据
        :param type_: 类型
        :param id_: id，user_id 或 group_id
        """
        for x in self._data[type_].keys():
            if self._data[type_][x].get("id") == id_:
                del self._data[type_][x]
                break
        self.save()

    def get_group_id(self, id_: int) -> Optional[int]:
        """
        通过id获取群号
        :param id_: id
        """
        return self._data["group"].get(id_)

    async def approve(self, bot: Bot, id_: int, type_: str) -> Optional[int]:
        """
        同意请求
        :param bot: Bot
        :param id_: id
        :param type_: 类型，private 或 group
        """
        return await self._set_add_request(bot, id_, type_, True)

    async def refused(self, bot: Bot, id_: int, type_: str) -> Optional[int]:
        """
        拒绝请求
        :param bot: Bot
        :param id_: id
        :param type_: 类型，private 或 group
        """
        return await self._set_add_request(bot, id_, type_, False)

    def clear(self):
        """
        清空所有请求信息，无视请求
        """
        self._data = {"private": {}, "group": {}}
        self.save()

    def set_group_name(self, group_name: str, group_id: int):
        """
        设置群聊名称
        :param group_name: 名称
        :param group_id: id
        """
        for id_ in self._data["group"].keys():
            if self._data["group"][id_]["invite_group"] == group_id:
                self._data["group"][id_]["group_name"] = group_name
                break
        self.save()

    async def show(self, type_: str) -> Optional[str]:
        """
        请求可视化
        """
        data = self._data[type_]
        if not data:
            return None
        img_list = []
        id_list = list(data.keys())
        id_list.reverse()
        for id_ in id_list:
            age = data[id_]["age"]
            nickname = data[id_]["nickname"]
            comment = data[id_]["comment"] if type_ == "private" else ""
            from_ = data[id_]["from"]
            sex = data[id_]["sex"]
            ava = BuildImage(
                80, 80, background=BytesIO(await get_user_avatar(data[id_]["id"]))
            )
            ava.circle()
            age_bk = BuildImage(
                len(str(age)) * 10 - 5,
                15,
                color="#04CAF7" if sex == "male" else "#F983C1",
            )
            age_bk.text((3, 1), f"{age}", fill=(255, 255, 255))
            x = BuildImage(
                90, 32, font_size=15, color="#EEEFF4", font="HYWenHei-85W.ttf"
            )
            x.text((0, 0), "同意/拒绝", center_type="center")
            x.circle_corner(10)
            A = BuildImage(500, 100, font_size=24, font="msyh.ttf")
            A.paste(ava, (15, 0), alpha=True, center_type="by_height")
            A.text((120, 15), nickname)
            A.paste(age_bk, (120, 50), True)
            A.paste(
                BuildImage(
                    200,
                    0,
                    font_size=12,
                    plain_text=f"对方留言：{comment}",
                    font_color=(140, 140, 143),
                ),
                (120 + age_bk.w + 10, 49),
                True,
            )
            if type_ == "private":
                A.paste(
                    BuildImage(
                        200,
                        0,
                        font_size=12,
                        plain_text=f"来源：{from_}",
                        font_color=(140, 140, 143),
                    ),
                    (120, 70),
                    True,
                )
            else:
                A.paste(
                    BuildImage(
                        200,
                        0,
                        font_size=12,
                        plain_text=f"邀请你加入：{data[id_]['group_name']}({data[id_]['invite_group']})",
                        font_color=(140, 140, 143),
                    ),
                    (120, 70),
                    True,
                )
            A.paste(x, (380, 35), True)
            A.paste(
                BuildImage(
                    0,
                    0,
                    plain_text=f"id：{id_}",
                    font_size=13,
                    font_color=(140, 140, 143),
                ),
                (400, 10),
                True,
            )
            img_list.append(A)
        A = BuildImage(500, len(img_list) * 100, 500, 100)
        for img in img_list:
            A.paste(img)
        bk = BuildImage(A.w, A.h + 50, color="#F8F9FB", font_size=20)
        bk.paste(A, (0, 50))
        bk.text(
            (15, 13), "好友请求" if type_ == "private" else "群聊请求", fill=(140, 140, 143)
        )
        return bk.pic2bs4()

    async def _set_add_request(
        self, bot: Bot, id_: int, type_: str, approve: bool
    ) -> Optional[int]:
        """
        处理请求
        :param bot: Bot
        :param id_: id
        :param type_: 类型，private 或 group
        :param approve: 是否同意
        """
        id_ = str(id_)
        if id_ in self._data[type_]:
            try:
                if type_ == "private":
                    await bot.set_friend_add_request(
                        flag=self._data[type_][id_]["flag"], approve=approve
                    )
                    rid = self._data[type_][id_]["id"]
                else:
                    await bot.set_group_add_request(
                        flag=self._data[type_][id_]["flag"],
                        sub_type="invite",
                        approve=approve,
                    )
                    rid = self._data[type_][id_]["invite_group"]
            except ActionFailed:
                logger.info(
                    f"同意{self._data[type_][id_]['nickname']}({self._data[type_][id_]['id']})"
                    f"的{'好友' if type_ == 'private' else '入群'}请求失败了..."
                )
                return None
            logger.info(
                f"同意{self._data[type_][id_]['nickname']}({self._data[type_][id_]['id']})"
                f"的{'好友' if type_ == 'private' else '入群'}请求..."
            )
            del self._data[type_][id_]
            self.save()
            return rid
        return None
