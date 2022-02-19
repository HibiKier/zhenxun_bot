import psutil
import time
from datetime import datetime
from utils.http_utils import AsyncHttpx
from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
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
        rst = ""
        for user in psutil.users():
            rst += f'[{user.name}] {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(user.started))}\n'
        self.user = rst[:-1]

    async def show(self):
        await self.check_all()
        A = BuildImage(0, 0, font_size=24)
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
        A = BuildImage(width + 50, height + 10, font_size=24, font="HWZhongSong.ttf")
        A.transparent(1)
        A.text((10, 10), rst)
        _x = max(width, height)
        bk = BuildImage(_x + 100, _x + 100, background=IMAGE_PATH / "background" / "check" / "0.jpg")
        bk.paste(A, alpha=True, center_type='center')
        return bk.pic2bs4()
