import psutil
import aiohttp
import time
from datetime import datetime
from utils.user_agent import get_user_agent
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientConnectorError
from utils.utils import get_local_proxy
from utils.image_utils import CreateImg
from configs.path_config import IMAGE_PATH
from pathlib import Path
import asyncio
from services.log import logger


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
        async with aiohttp.ClientSession(headers=get_user_agent()) as session:
            try:
                async with session.get(
                    "https://www.baidu.com/", proxy=get_local_proxy(), timeout=3
                ) as response:
                    pass
            except (TimeoutError, ClientConnectorError) as e:
                logger.warning(f"访问BaiDu失败... e: {e}")
                self.baidu = 404
            try:
                async with session.get(
                    "https://www.google.com/", proxy=get_local_proxy(), timeout=3
                ) as response:
                    pass
            except (TimeoutError, ClientConnectorError) as e:
                logger.warning(f"访问Google失败... e: {e}")
                self.google = 404

    def check_user(self):
        rst = ""
        for user in psutil.users():
            rst += f'[{user.name}] {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(user.started))}\n'
        self.user = rst[:-1]

    async def show(self):
        await self.check_all()
        A = CreateImg(0, 0, font_size=24)
        rst = (
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
            rst += "-----User-----\n" + self.user
        width = 0
        height = 0
        for x in rst.split('\n'):
            w, h = A.getsize(x)
            if w > width:
                width = w
            height += 30
        A = CreateImg(width + 50, height + 10, font_size=24, font="HWZhongSong.ttf")
        A.transparent(1)
        A.text((10, 10), rst)
        _x = max(width, height)
        bk = CreateImg(_x + 100, _x + 100, background=Path(IMAGE_PATH) / "background" / "check" / "0.jpg")
        bk.paste(A, alpha=True, center_type='center')
        return bk.pic2bs4()
