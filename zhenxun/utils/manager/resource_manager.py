import os
from pathlib import Path
import shutil
import zipfile

from zhenxun.configs.path_config import FONT_PATH
from zhenxun.services.log import logger
from zhenxun.utils.github_utils import GithubUtils
from zhenxun.utils.http_utils import AsyncHttpx

CMD_STRING = "ResourceManager"


class DownloadResourceException(Exception):
    pass


class ResourceManager:
    GITHUB_URL = "https://github.com/zhenxun-org/zhenxun-bot-resources/tree/main"

    RESOURCE_PATH = Path() / "resources"

    TMP_PATH = Path() / "_resource_tmp"

    ZIP_FILE = TMP_PATH / "resources.zip"

    UNZIP_PATH = None

    @classmethod
    async def init_resources(cls, force: bool = False):
        if (FONT_PATH.exists() and os.listdir(FONT_PATH)) and not force:
            return
        if cls.TMP_PATH.exists():
            logger.debug(
                "resources临时文件夹已存在，移除resources临时文件夹", CMD_STRING
            )
            shutil.rmtree(cls.TMP_PATH)
        cls.TMP_PATH.mkdir(parents=True, exist_ok=True)
        try:
            await cls.__download_resources()
            cls.file_handle()
        except Exception as e:
            logger.error("获取resources资源包失败", CMD_STRING, e=e)
        if cls.TMP_PATH.exists():
            logger.debug("移除resources临时文件夹", CMD_STRING)
            shutil.rmtree(cls.TMP_PATH)

    @classmethod
    def file_handle(cls):
        if not cls.UNZIP_PATH:
            return
        cls.__recursive_folder(cls.UNZIP_PATH, "resources")

    @classmethod
    def __recursive_folder(cls, dir: Path, parent_path: str):
        for file in dir.iterdir():
            if file.is_dir():
                cls.__recursive_folder(file, f"{parent_path}/{file.name}")
            else:
                res_file = Path(parent_path) / file.name
                if res_file.exists():
                    res_file.unlink()
                res_file.parent.mkdir(parents=True, exist_ok=True)
                file.rename(res_file)

    @classmethod
    async def __download_resources(cls):
        """获取resources文件夹"""
        repo_info = GithubUtils.parse_github_url(cls.GITHUB_URL)
        url = await repo_info.get_archive_download_urls()
        logger.debug("开始下载resources资源包...", CMD_STRING)
        if not await AsyncHttpx.download_file(url, cls.ZIP_FILE, stream=True):
            logger.error(
                "下载resources资源包失败，请尝试重启重新下载或前往 "
                "https://github.com/zhenxun-org/zhenxun-bot-resources 手动下载..."
            )
            raise DownloadResourceException("下载resources资源包失败...")
        logger.debug("下载resources资源文件压缩包完成...", CMD_STRING)
        tf = zipfile.ZipFile(cls.ZIP_FILE)
        tf.extractall(cls.TMP_PATH)
        logger.debug("解压文件压缩包完成...", CMD_STRING)
        download_file_path = cls.TMP_PATH / next(
            x for x in os.listdir(cls.TMP_PATH) if (cls.TMP_PATH / x).is_dir()
        )
        cls.UNZIP_PATH = download_file_path / "resources"
        if tf:
            tf.close()
