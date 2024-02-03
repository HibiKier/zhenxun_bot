import os
from pathlib import Path

import httpx

from zhenxun.services.log import logger


class ResourceDirManager:
    """
    临时文件管理器
    """

    temp_path = []

    @classmethod
    def __tree_append(cls, path: Path):
        """递归添加文件夹

        参数:
            path: 文件夹路径
        """
        for f in os.listdir(path):
            file = path / f
            if file.is_dir():
                if file not in cls.temp_path:
                    cls.temp_path.append(file)
                    logger.debug(f"添加临时文件夹: {path}")
                cls.__tree_append(file)

    @classmethod
    def add_temp_dir(cls, path: str | Path, tree: bool = False):
        """添加临时清理文件夹，这些文件夹会被自动清理

        参数:
            path: 文件夹路径
            tree: 是否递归添加文件夹
        """
        if isinstance(path, str):
            path = Path(path)
        if path not in cls.temp_path:
            cls.temp_path.append(path)
            logger.debug(f"添加临时文件夹: {path}")
        if tree:
            cls.__tree_append(path)


async def get_user_avatar(uid: int | str) -> bytes | None:
    """快捷获取用户头像

    参数:
        uid: 用户id
    """
    url = f"http://q1.qlogo.cn/g?b=qq&nk={uid}&s=160"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except Exception as e:
                logger.error("获取用户头像错误", "Util", target=uid)
    return None


async def get_group_avatar(gid: int | str) -> bytes | None:
    """快捷获取用群头像

    参数:
        :param gid: 群号
    """
    url = f"http://p.qlogo.cn/gh/{gid}/{gid}/640/"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except Exception as e:
                logger.error("获取群头像错误", "Util", target=gid)
    return None
