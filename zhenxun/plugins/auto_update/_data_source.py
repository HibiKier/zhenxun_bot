import os
import shutil
import tarfile
import zipfile
from pathlib import Path

from nonebot.adapters import Bot
from nonebot.utils import run_sync

from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.platform import PlatformUtils

from .config import (
    BACKUP_PATH,
    BASE_PATH,
    DEV_URL,
    DOWNLOAD_GZ_FILE,
    DOWNLOAD_ZIP_FILE,
    MAIN_URL,
    PYPROJECT_FILE,
    PYPROJECT_LOCK_FILE,
    RELEASE_URL,
    REPLACE_FOLDERS,
    TMP_PATH,
    VERSION_FILE,
)


@run_sync
def _file_handle(latest_version: str | None):
    """文件移动操作

    参数:
        latest_version: 版本号
    """
    BACKUP_PATH.mkdir(exist_ok=True, parents=True)
    logger.debug("开始解压文件压缩包...", "检查更新")
    download_file = DOWNLOAD_GZ_FILE
    if DOWNLOAD_GZ_FILE.exists():
        tf = tarfile.open(DOWNLOAD_GZ_FILE)
    else:
        download_file = DOWNLOAD_ZIP_FILE
        tf = zipfile.ZipFile(DOWNLOAD_ZIP_FILE)
    tf.extractall(TMP_PATH)
    logger.debug("解压文件压缩包完成...", "检查更新")
    download_file_path = (
        TMP_PATH / [x for x in os.listdir(TMP_PATH) if (TMP_PATH / x).is_dir()][0]
    )
    _pyproject = download_file_path / "pyproject.toml"
    _lock_file = download_file_path / "poetry.lock"
    extract_path = download_file_path / "zhenxun"
    target_path = BASE_PATH
    if PYPROJECT_FILE.exists():
        logger.debug(f"移除备份文件: {PYPROJECT_FILE}", "检查更新")
        shutil.move(PYPROJECT_FILE, BACKUP_PATH / "pyproject.toml")
    if PYPROJECT_LOCK_FILE.exists():
        logger.debug(f"移除备份文件: {PYPROJECT_FILE}", "检查更新")
        shutil.move(PYPROJECT_LOCK_FILE, BACKUP_PATH / "poetry.lock")
    if _pyproject.exists():
        logger.debug("移动文件: pyproject.toml", "检查更新")
        shutil.move(_pyproject, Path() / "pyproject.toml")
    if _lock_file.exists():
        logger.debug("移动文件: pyproject.toml", "检查更新")
        shutil.move(_lock_file, Path() / "poetry.lock")
    for folder in REPLACE_FOLDERS:
        """移动指定文件夹"""
        _dir = BASE_PATH / folder
        _backup_dir = BACKUP_PATH / folder
        if _backup_dir.exists():
            logger.debug(f"删除备份文件夹 {_backup_dir}", "检查更新")
            shutil.rmtree(_backup_dir)
        if _dir.exists():
            logger.debug(f"移动旧文件夹 {_dir}", "检查更新")
            shutil.move(_dir, _backup_dir)
        else:
            logger.warning(f"文件夹 {_dir} 不存在，跳过删除", "检查更新")
    for folder in REPLACE_FOLDERS:
        src_folder_path = extract_path / folder
        dest_folder_path = target_path / folder
        if src_folder_path.exists():
            logger.debug(
                f"移动文件夹: {src_folder_path} -> {dest_folder_path}", "检查更新"
            )
            shutil.move(src_folder_path, dest_folder_path)
        else:
            logger.debug(f"源文件夹不存在: {src_folder_path}", "检查更新")
    if download_file.exists():
        logger.debug(f"删除下载文件: {download_file}", "检查更新")
        download_file.unlink()
    if extract_path.exists():
        logger.debug(f"删除解压文件夹: {extract_path}", "检查更新")
        shutil.rmtree(extract_path)
    if tf:
        tf.close()
    if TMP_PATH.exists():
        shutil.rmtree(TMP_PATH)
    if latest_version:
        with open(VERSION_FILE, "w", encoding="utf8") as f:
            f.write(f"__version__: {latest_version}")
    os.system(f"poetry install --directory={Path().absolute()}")


class UpdateManage:

    @classmethod
    async def check_version(cls) -> str:
        """检查更新版本

        返回:
            str: 更新信息
        """
        cur_version = cls.__get_version()
        data = await cls.__get_latest_data()
        if not data:
            return "检查更新获取版本失败..."
        return f"检测到当前版本更新\n当前版本：{cur_version}\n最新版本：{data.get('name')}\n创建日期：{data.get('created_at')}\n更新内容：\n{data.get('body')}"

    @classmethod
    async def update(cls, bot: Bot, user_id: str, version_type: str) -> str | None:
        """更新操作

        参数:
            bot: Bot
            user_id: 用户id
            version_type: 更新版本类型

        返回:
            str | None: 返回消息
        """
        logger.info(f"开始下载真寻最新版文件....", "检查更新")
        cur_version = cls.__get_version()
        new_version = "main"
        url = MAIN_URL
        if version_type == "dev":
            url = DEV_URL
            new_version = "dev"
        if version_type == "release":
            data = await cls.__get_latest_data()
            if not data:
                return "获取更新版本失败..."
            url = data.get("tarball_url")
            new_version = data.get("name")
            url = (await AsyncHttpx.get(url)).headers.get("Location")  # type: ignore
        if not url:
            return "获取版本下载链接失败..."
        if TMP_PATH.exists():
            logger.debug(f"删除临时文件夹 {TMP_PATH}", "检查更新")
            shutil.rmtree(TMP_PATH)
        logger.debug(
            f"开始更新版本：{cur_version} -> {new_version} | 下载链接：{url}",
            "检查更新",
        )
        await PlatformUtils.send_superuser(
            bot,
            f"检测真寻已更新，版本更新：{cur_version} -> {new_version}\n开始更新...",
            user_id,
        )
        download_file = (
            DOWNLOAD_GZ_FILE if version_type == "release" else DOWNLOAD_ZIP_FILE
        )
        if await AsyncHttpx.download_file(url, download_file):
            logger.debug("下载真寻最新版文件完成...", "检查更新")
            if version_type != "release":
                new_version = None
            await _file_handle(new_version)
            return f"版本更新完成\n版本: {cur_version} -> {new_version}\n请重新启动真寻以完成更新!"
        else:
            logger.debug("下载真寻最新版文件失败...", "检查更新")
        return None

    @classmethod
    def __get_version(cls) -> str:
        """获取当前版本

        返回:
            str: 当前版本号
        """
        _version = "v0.0.0"
        if VERSION_FILE.exists():
            text = VERSION_FILE.open(encoding="utf8").readline()
            if text:
                _version = text.split(":")[-1].strip()
        return _version

    @classmethod
    async def __get_latest_data(cls) -> dict:
        """获取最新版本信息

        返回:
            dict: 最新版本数据
        """
        for _ in range(3):
            try:
                res = await AsyncHttpx.get(RELEASE_URL)
                if res.status_code == 200:
                    return res.json()
            except TimeoutError:
                pass
            except Exception as e:
                logger.error(f"检查更新真寻获取版本失败", e=e)
        return {}
