import psutil
import aiohttp
import time
from datetime import datetime
from utils.user_agent import get_user_agent
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ClientConnectorError
from utils.utils import get_local_proxy
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
        return rst
