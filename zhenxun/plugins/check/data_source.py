import asyncio
import time
from datetime import datetime

import psutil

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.image_utils import BuildImage


class Check:
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.disk = None
        self.user = None
        self.baidu = 200
        self.google = 200

    async def check_all(self):
        await self.check_network()
        await asyncio.sleep(0.1)
        self.check_system()
        self.check_user()

    def check_system(self):
        self.cpu = psutil.cpu_percent()
        self.memory = psutil.virtual_memory().percent
        self.disk = psutil.disk_usage("/").percent

    async def check_network(self):
        try:
            await AsyncHttpx.get("https://www.baidu.com/", timeout=5)
        except Exception as e:
            logger.warning(f"访问BaiDu失败... {type(e)}: {e}")
            self.baidu = 404
        try:
            await AsyncHttpx.get("https://www.google.com/", timeout=5)
        except Exception as e:
            logger.warning(f"访问Google失败... {type(e)}: {e}")
            self.google = 404

    def check_user(self):
        result = ""
        for user in psutil.users():
            result += f'[{user.name}] {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(user.started))}\n'
        self.user = result[:-1]

    async def show(self) -> BuildImage:
        await self.check_all()
        font = BuildImage.load_font(font_size=24)
        result = (
            f'[Time] {str(datetime.now()).split(".")[0]}\n'
            f"-----System-----\n"
            f"[CPU] {self.cpu}%\n"
            f"[Memory] {self.memory}%\n"
            f"[Disk] {self.disk}%\n"
            f"-----Network-----\n"
            f"[BaiDu] {self.baidu}\n"
            f"[Google] {self.google}\n"
        )
        if self.user:
            result += "-----User-----\n" + self.user
        width = 0
        height = 0
        for x in result.split("\n"):
            w, h = BuildImage.get_text_size(x, font)
            if w > width:
                width = w
            height += 30
        A = BuildImage(width + 50, height + 10, font_size=24)
        await A.transparent(1)
        await A.text((10, 10), result)
        max_width = max(width, height)
        bk = BuildImage(
            max_width + 100,
            max_width + 100,
            background=IMAGE_PATH / "background" / "check" / "0.jpg",
        )
        await bk.paste(A, center_type="center")
        return bk
