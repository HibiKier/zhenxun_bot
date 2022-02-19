from nonebot.adapters.onebot.v11 import Bot, Message
from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from utils.http_utils import AsyncHttpx
from typing import List
from services.log import logger
from pathlib import Path
import ujson as json
import nonebot
import asyncio
import platform
import tarfile
import shutil
import os

if str(platform.system()).lower() == "windows":
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)


driver = nonebot.get_driver()

release_url = "https://api.github.com/repos/HibiKier/zhenxun_bot/releases/latest"

_version_file = Path() / "__version__"
zhenxun_latest_tar_gz = Path() / "zhenxun_latest_file.tar.gz"
temp_dir = Path() / "temp"
backup_dir = Path() / "backup"


@driver.on_bot_connect
async def remind(bot: Bot):
    if str(platform.system()).lower() != "windows":
        restart = Path() / "restart.sh"
        if not restart.exists():
            with open(restart, "w", encoding="utf8") as f:
                f.write(
                    f"pid=$(netstat -tunlp | grep "
                    + str(bot.config.port)
                    + " | awk '{print $7}')\n"
                    "pid=${pid%/*}\n"
                    "kill -9 $pid\n"
                    "sleep 3\n"
                    "python3 bot.py"
                )
            os.system("chmod +x ./restart.sh")
            logger.info("已自动生成 restart.sh(重启) 文件，请检查脚本是否与本地指令符合...")
    is_restart_file = Path() / "is_restart"
    if is_restart_file.exists():
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]),
            message=f"真寻重启完毕...",
        )
        is_restart_file.unlink()


async def check_update(bot: Bot) -> 'int, str':
    logger.info("开始检查更新真寻酱....")
    _version = "v0.0.0"
    if _version_file.exists():
        _version = (
            open(_version_file, "r", encoding="utf8").readline().split(":")[-1].strip()
        )
    data = await get_latest_version_data()
    if data:
        latest_version = data["name"]
        if _version != latest_version:
            tar_gz_url = data["tarball_url"]
            logger.info(f"检测真寻已更新，当前版本：{_version}，最新版本：{latest_version}")
            await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message=f"检测真寻已更新，当前版本：{_version}，最新版本：{latest_version}\n" f"开始更新.....",
            )
            logger.info(f"开始下载真寻最新版文件....")
            if await AsyncHttpx.download_file(tar_gz_url, zhenxun_latest_tar_gz):
                logger.info("下载真寻最新版文件完成....")
                error = await asyncio.get_event_loop().run_in_executor(
                    None, _file_handle, latest_version
                )
                if error:
                    return 998, error
                logger.info("真寻更新完毕，清理文件完成....")
                logger.info("开始获取真寻更新日志.....")
                update_info = data["body"]
                width = 0
                height = len(update_info.split('\n')) * 24
                A = BuildImage(width, height, font_size=20)
                for m in update_info.split('\n'):
                    w, h = A.getsize(m)
                    if w > width:
                        width = w
                A = BuildImage(width + 50, height, font_size=20)
                A.text((10, 10), update_info)
                A.save(f'{IMAGE_PATH}/update_info.png')
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=Message(f"真寻更新完成，版本：{_version} -> {latest_version}\n"
                                    f"更新日期：{data['created_at']}\n"
                                    f"更新日志：\n"
                                    f"{image('update_info.png')}"),
                )
                return 200, ''
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
    return 999, ''


def _file_handle(latest_version: str) -> str:
    if not temp_dir.exists():
        temp_dir.mkdir(exist_ok=True, parents=True)
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    tf = None
    error = ''
    # try:
    backup_dir.mkdir(exist_ok=True, parents=True)
    logger.info("开始解压真寻文件压缩包....")
    tf = tarfile.open(zhenxun_latest_tar_gz)
    tf.extractall(temp_dir)
    logger.info("解压真寻文件压缩包完成....")
    zhenxun_latest_file = Path(temp_dir) / os.listdir(temp_dir)[0]
    update_info_file = Path(zhenxun_latest_file) / "update_info.json"
    update_info = json.load(open(update_info_file, "r", encoding="utf8"))
    update_file = update_info["update_file"]
    add_file = update_info["add_file"]
    delete_file = update_info["delete_file"]
    config_file = Path() / "configs" / "config.py"
    config_path_file = Path() / "configs" / "path_config.py"
    for file in [config_file.name]:
        tmp = ""
        new_file = Path(zhenxun_latest_file) / "configs" / file
        old_file = Path() / "configs" / file
        new_lines = open(new_file, "r", encoding="utf8").readlines()
        old_lines = open(old_file, "r", encoding="utf8").readlines()
        for nl in new_lines:
            tmp += check_old_lines(old_lines, nl)
        with open(old_file, "w", encoding="utf8") as f:
            f.write(tmp)
    for file in delete_file + update_file:
        if file != "configs":
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
        if old_file not in [config_file, config_path_file] and file != "configs":
            if not old_file.exists() and new_file.exists():
                os.rename(new_file.absolute(), old_file.absolute())
                logger.info(f"已更新文件：{file}")
    # except Exception as e:
    #     error = f'{type(e)}：{e}'
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
    return error


# 获取最新版本号
async def get_latest_version_data() -> dict:
    for _ in range(3):
        try:
            res = await AsyncHttpx.get(release_url)
            if res.status_code == 200:
                return res.json()
        except TimeoutError:
            pass
        except Exception as e:
            logger.error(f"检查更新真寻获取版本失败 {type(e)}：{e}")
    return {}


# 逐行检测
def check_old_lines(lines: List[str], line: str) -> str:
    if "=" not in line:
        return line
    for l in lines:
        if "=" in l and l.split("=")[0].strip() == line.split("=")[0].strip():
            return l
    return line
