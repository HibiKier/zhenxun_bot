from aiohttp.client_exceptions import ClientConnectorError
from nonebot.adapters.cqhttp import Bot
from utils.user_agent import get_user_agent
from utils.utils import get_local_proxy, get_bot
from typing import List
from bs4.element import Tag
from services.log import logger
from bs4 import BeautifulSoup
from pathlib import Path
import ujson as json
import nonebot
import asyncio
import aiofiles
import aiohttp
import platform
import tarfile
import shutil
import os

if str(platform.system()).lower() == "windows":
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)


driver = nonebot.get_driver()

version_url = "https://github.com/HibiKier/zhenxun_bot/releases"
main_url = "https://github.com/HibiKier/zhenxun_bot"

_version_file = Path() / "__version__"
zhenxun_latest_tar_gz = Path() / "zhenxun_latest_file.tar.gz"
temp_dir = Path() / "temp"
backup_dir = Path() / "backup"


@driver.on_startup
def init():
    if str(platform.system()).lower() != "windows":
        restart = Path() / "restart.sh"
        env_file = Path() / ".env.dev"
        if not restart.exists() and env_file.exists():
            with open(env_file, "r", encoding="utf8") as ef:
                data = ef.readlines()
            port = [x.split("=")[1].strip() for x in data if "port" in x.lower()][0]
            with open(restart, "w", encoding="utf8") as f:
                f.write(
                    "pid=$(netstat -tunlp | grep " + port + " | awk '{print $7}')\n"
                    "pid=${pid%/*}\n"
                    "kill -9 $pid\n"
                    "sleep 3\n"
                    "python3 bot.py"
                )
            os.system("chmod +x ./restart.sh")
            logger.info("已自动生成 restart.sh(重启) 文件，请检查是否与本地指令符合...")


@driver.on_bot_connect
async def remind(bot: Bot):
    is_restart_file = Path() / 'is_restart'
    if is_restart_file.exists():
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]),
            message=f"真寻重启完毕...",
        )
        is_restart_file.unlink()


async def check_update(bot: Bot) -> int:
    logger.info("开始检查更新真寻酱....")
    _version = "v0.0.0"
    if _version_file.exists():
        _version = (
            open(_version_file, "r", encoding="utf8").readline().split(":")[-1].strip()
        )
    latest_version, tar_gz_url = await get_latest_version()
    if latest_version and tar_gz_url:
        if _version != latest_version:
            logger.info(f"检测真寻已更新，当前版本：{_version}，最新版本：{latest_version}")
            await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message=f"检测真寻已更新，当前版本：{_version}，最新版本：{latest_version}\n" f"开始更新.....",
            )
            logger.info(f"开始下载真寻最新版文件....")
            if await download_latest_file(tar_gz_url):
                logger.info("下载真寻最新版文件完成....")
                await asyncio.get_event_loop().run_in_executor(
                    None, _file_handle, latest_version
                )
                logger.info("真寻更新完毕，清理文件完成....")
                logger.info("开始获取真寻更新日志.....")
                update_info = await get_updated_info()
                if update_info:
                    logger.info("获取真寻更新日志成功...开始发送日志...")
                    await bot.send_private_msg(
                        user_id=int(list(bot.config.superusers)[0]),
                        message=f"真寻更新完成，版本：{_version} -> {latest_version}\n"
                        f"更新日志：\n"
                        f"{update_info}",
                    )
                else:
                    logger.warning("获取真寻更新日志失败...")
                    await bot.send_private_msg(
                        user_id=int(list(bot.config.superusers)[0]),
                        message=f"真寻更新完成，版本：{_version} -> {latest_version}\n"
                        f"获取真寻更新日志失败...",
                    )
                return 200
            else:
                logger.warning(f"下载真寻最新版本失败...版本号：{latest_version}")
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=f"下载真寻最新版本失败...版本号：{latest_version}.",
                )
        else:
            logger.info(f"自动获取真寻版本成功：{latest_version}，当前版本为最新版，无需更新...")
            await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message=f"自动获取真寻版本成功：{latest_version}，当前版本为最新版，无需更新...",
            )
    else:
        logger.warning("自动获取真寻版本失败....")
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]), message=f"自动获取真寻版本失败...."
        )
    return 999


def _file_handle(latest_version: str):
    if not temp_dir.exists():
        temp_dir.mkdir(exist_ok=True, parents=True)
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    backup_dir.mkdir(exist_ok=True, parents=True)
    logger.info("开始解压真寻文件压缩包....")
    tf = tarfile.open(zhenxun_latest_tar_gz)
    tf.extractall(temp_dir)
    logger.info("解压真寻文件压缩包完成....")
    zhenxun_latest_file = Path(temp_dir) / f"zhenxun_bot-{latest_version[1:]}"
    update_info_file = Path(zhenxun_latest_file) / "update_info.json"
    update_info = json.load(open(update_info_file, "r", encoding="utf8"))
    update_file = update_info["update_file"]
    add_file = update_info["add_file"]
    delete_file = update_info["delete_file"]
    config_file = Path() / "configs" / "config.py"
    config_path_file = Path() / "configs" / "config_path.py"
    for file in delete_file + update_file:
        file = Path() / file
        backup_file = Path(backup_dir) / file
        if file.exists():
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            if backup_file.exists():
                backup_file.unlink()
            if file not in [config_file, config_path_file]:
                os.rename(file.absolute(), backup_file.absolute())
            else:
                with open(file, "r", encoding="utf8") as rf:
                    data = rf.read()
                with open(backup_file, "w", encoding="utf8") as wf:
                    wf.write(data)
            logger.info(f"已备份文件：{file}")
    for file in add_file + update_file:
        new_file = Path(zhenxun_latest_file) / file
        old_file = Path() / file
        if old_file not in [config_file, config_path_file]:
            if not old_file.exists() and new_file.exists():
                os.rename(new_file.absolute(), old_file.absolute())
                logger.info(f"已更新文件：{file}")
        else:
            tmp = ""
            new_lines = open(new_file, "r", encoding="utf8").readlines()
            old_lines = open(old_file, "r", encoding="utf8").readlines()
            for nl in new_lines:
                tmp += check_old_lines(old_lines, nl)
            with open(file, "w", encoding="utf8") as f:
                f.write(tmp)
    if tf:
        tf.close()
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    if zhenxun_latest_tar_gz.exists():
        zhenxun_latest_tar_gz.unlink()
    local_update_info_file = Path() / "update_info.json"
    if local_update_info_file.exists():
        local_update_info_file.unlink()
    with open(_version_file, "w", encoding="utf8") as f:
        f.write(f"__version__: {latest_version}")


# 获取最新版本号
async def get_latest_version() -> "str, str":
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        for _ in range(3):
            try:
                async with session.get(version_url, proxy=get_local_proxy()) as res:
                    if res.status == 200:
                        soup = BeautifulSoup(await res.text(), "lxml")
                        div = soup.find("div", {"class": "release-entry"})
                        latest_version = (
                            div.find(
                                "div", {"class": "f1 flex-auto min-width-0 text-normal"}
                            )
                            .find("a")
                            .text
                        )
                        tar_gz_url = div.find_all(
                            "a", {"class": "d-flex flex-items-center"}
                        )[-1].get("href")
                        tar_gz_url = f"https://github.com{tar_gz_url}"
                        return latest_version, tar_gz_url
            except (TimeoutError, ClientConnectorError):
                pass
    return "", ""


# 下载文件
async def download_latest_file(url_: str) -> bool:
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        for _ in range(3):
            try:
                async with session.get(url_, proxy=get_local_proxy()) as res:
                    if res.status == 200:
                        async with aiofiles.open(zhenxun_latest_tar_gz, "wb") as f:
                            await f.write(await res.read())
                            return True
            except (TimeoutError, ClientConnectorError):
                pass
    return False


# 逐行检测
def check_old_lines(lines: List[str], line: str) -> str:
    if "=" not in line:
        return line
    for l in lines:
        if "=" in l and l.split("=")[0].strip() == line.split("=")[0].strip():
            if len(l) > len(line):
                return l
    return line


async def get_updated_info() -> str:
    async with aiohttp.ClientSession(headers=get_user_agent()) as session:
        for _ in range(3):
            try:
                async with session.get(main_url, proxy=get_local_proxy()) as res:
                    soup = BeautifulSoup(await res.text(), "lxml")
                    children_list = list(soup.find("article").children)
                    children_list = [x for x in children_list if x != "\n"]
                    for i, children in enumerate(children_list):
                        a = children.find("a")
                        if a and isinstance(a, Tag) and a.get("href") == "#更新":
                            update_info = ""
                            tmp_children_list = children_list[i:]
                            tmp_children_list = [
                                x for x in tmp_children_list if "ul" in str(x)
                            ]
                            for j, chi in enumerate(tmp_children_list):
                                if "ul" in str(chi):
                                    update_time = children_list[i:][j + 1].text
                                    update_info += f"更新日期：{update_time}\n"
                                    ul = children_list[i:][j + 2]
                                    break
                            for li in ul.find_all("li"):
                                update_info += f"\t● {li.text}\n"
                            return update_info
            except (TimeoutError, ClientConnectorError):
                pass
    return ""
