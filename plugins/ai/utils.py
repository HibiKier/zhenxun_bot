from utils.manager import StaticData
from configs.config import NICKNAME
from models.ban_user import BanUser
from typing import Optional
import random
import time


class AiMessageManager(StaticData):
    def __init__(self):
        super().__init__(None)
        self._same_message = [
            "为什么要发一样的话？",
            "请不要再重复对我说一句话了，不然我就要生气了！",
            "别再发这句话了，我已经知道了...",
            "你是只会说这一句话吗？",
            "[*]，你发我也发！",
            "[uname]，[*]",
            f"救命！有笨蛋一直给{NICKNAME}发一样的话！",
            "这句话你已经给我发了{}次了，再发就生气！",
        ]
        self._repeat_message = [
            f"请不要学{NICKNAME}说话",
            f"为什么要一直学{NICKNAME}说话？",
            "你再学！你再学我就生气了！",
            f"呜呜，你是想欺负{NICKNAME}嘛..",
            "[uname]不要再学我说话了！",
            "再学我说话，我就把你拉进黑名单（生气",
            "你再学！[uname]是个笨蛋！",
            "你已经学我说话{}次了！别再学了！",
        ]

    def add_message(self, user_id: int, message: str):
        """
        添加用户消息
        :param user_id: 用户id
        :param message: 消息内容
        """
        if message:
            if self._data.get(user_id) is None:
                self._data[user_id] = {
                    "time": time.time(),
                    "message": [],
                    "result": [],
                    "repeat_count": 0,
                }
            if time.time() - self._data[user_id]["time"] > 60 * 10:
                self._data[user_id]["message"].clear()
            self._data[user_id]["time"] = time.time()
            self._data[user_id]["message"].append(message.strip())

    def add_result(self, user_id: int, message: str):
        """
        添加回复用户的消息
        :param user_id: 用户id
        :param message: 回复消息内容
        """
        if message:
            if self._data.get(user_id) is None:
                self._data[user_id] = {
                    "time": time.time(),
                    "message": [],
                    "result": [],
                    "repeat_count": 0,
                }
            if time.time() - self._data[user_id]["time"] > 60 * 10:
                self._data[user_id]["result"].clear()
                self._data[user_id]["repeat_count"] = 0
            self._data[user_id]["time"] = time.time()
            self._data[user_id]["result"].append(message.strip())

    async def get_result(self, user_id: int, nickname: str) -> Optional[str]:
        """
        特殊消息特殊回复
        :param user_id: 用户id
        :param nickname: 用户昵称
        """
        try:
            if len(self._data[user_id]["message"]) < 2:
                return None
        except KeyError:
            return None
        msg = await self._get_user_repeat_message_result(user_id)
        if not msg:
            msg = await self._get_user_same_message_result(user_id)
        if msg:
            if "[uname]" in msg:
                msg = msg.replace("[uname]", nickname)
            if not msg.startswith("生气了！你好烦，闭嘴！") and "[*]" in msg:
                msg = msg.replace("[*]", self._data[user_id]["message"][-1])
        return msg

    async def _get_user_same_message_result(self, user_id: int) -> Optional[str]:
        """
        重复消息回复
        :param user_id: 用户id
        """
        msg = self._data[user_id]["message"][-1]
        cnt = 0
        _tmp = self._data[user_id]["message"][:-1]
        _tmp.reverse()
        for s in _tmp:
            if s == msg:
                cnt += 1
            else:
                break
        if cnt > 1:
            if random.random() < 0.5 and cnt > 3:
                rand = random.randint(60, 300)
                await BanUser.ban(user_id, 9, rand)
                self._data[user_id]["message"].clear()
                return f"生气了！你好烦，闭嘴！给我老实安静{rand}秒"
            return random.choice(self._same_message).format(cnt)
        return None

    async def _get_user_repeat_message_result(self, user_id: int) -> Optional[str]:
        """
        复读真寻的消息回复
        :param user_id: 用户id
        """
        msg = self._data[user_id]["message"][-1]
        if self._data[user_id]["result"]:
            rst = self._data[user_id]["result"][-1]
        else:
            return None
        if msg == rst:
            self._data[user_id]["repeat_count"] += 1
            cnt = self._data[user_id]["repeat_count"]
            if cnt > 1:
                if random.random() < 0.5 and cnt > 3:
                    rand = random.randint(60, 300)
                    await BanUser.ban(user_id, 9, rand)
                    self._data[user_id]["result"].clear()
                    self._data[user_id]["repeat_count"] = 0
                    return f"生气了！你好烦，闭嘴！给我老实安静{rand}秒"
                return random.choice(self._repeat_message).format(cnt)
        return None


ai_message_manager = AiMessageManager()
