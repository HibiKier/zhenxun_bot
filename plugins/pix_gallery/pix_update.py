from nonebot import on_command
from utils.utils import is_number
from nonebot.permission import SUPERUSER
from ._data_source import start_update_image_url
from ._model.pixiv_keyword_user import PixivKeywordUser
from ._model.omega_pixiv_illusts import OmegaPixivIllusts
from ._model.pixiv import Pixiv
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
import time
from services.log import logger
from pathlib import Path
from typing import List
from datetime import datetime
import asyncio
import os


__zx_plugin_name__ = "pix检查更新 [Superuser]"
__plugin_usage__ = """
usage：
    更新pix收录的所有或指定数量的 关键词/uid/pid
    指令：
        更新pix关键词 *[keyword/uid/pid] [num=max]: 更新仅keyword/uid/pid或全部
        pix检测更新：检测从未更新过的uid和pid
        示例：更新pix关键词keyword
        示例：更新pix关键词uid 10
""".strip()
__plugin_des__ = "pix图库收录数据检查更新"
__plugin_cmd__ = ["更新pix关键词 *[keyword/uid/pid] [num=max]", "pix检测更新"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"

start_update = on_command(
    "更新pix关键词", aliases={"更新pix关键字"}, permission=SUPERUSER, priority=1, block=True
)

check_not_update_uid_pid = on_command(
    "pix检测更新",
    aliases={"pix检查更新"},
    permission=SUPERUSER,
    priority=1,
    block=True,
)

check_omega = on_command("检测omega图库", permission=SUPERUSER, priority=1, block=True)


@start_update.handle()
async def _(arg: Message = CommandArg()):
    msg_sp = arg.extract_plain_text().strip().split()
    _pass_keyword, _ = await PixivKeywordUser.get_current_keyword()
    _pass_keyword.reverse()
    black_pid = await PixivKeywordUser.get_black_pid()
    _keyword = [
        x
        for x in _pass_keyword
        if not x.startswith("uid:")
        and not x.startswith("pid:")
        and not x.startswith("black:")
    ]
    _uid = [x for x in _pass_keyword if x.startswith("uid:")]
    _pid = [x for x in _pass_keyword if x.startswith("pid:")]
    num = 9999
    msg = msg_sp[0] if len(msg_sp) else ""
    if len(msg_sp) == 2:
        if is_number(msg_sp[1]):
            num = int(msg_sp[1])
        else:
            await start_update.finish("参数错误...第二参数必须为数字")
    if num < 10000:
        keyword_str = "，".join(
            _keyword[: num if num < len(_keyword) else len(_keyword)]
        )
        uid_str = "，".join(_uid[: num if num < len(_uid) else len(_uid)])
        pid_str = "，".join(_pid[: num if num < len(_pid) else len(_pid)])
        if msg.lower() == "pid":
            update_lst = _pid
            info = f"开始更新Pixiv搜图PID：\n{pid_str}"
        elif msg.lower() == "uid":
            update_lst = _uid
            info = f"开始更新Pixiv搜图UID：\n{uid_str}"
        elif msg.lower() == "keyword":
            update_lst = _keyword
            info = f"开始更新Pixiv搜图关键词：\n{keyword_str}"
        else:
            update_lst = _pass_keyword
            info = f"开始更新Pixiv搜图关键词：\n{keyword_str}\n更新UID：{uid_str}\n更新PID：{pid_str}"
        num = num if num < len(update_lst) else len(update_lst)
    else:
        if msg.lower() == "pid":
            update_lst = [f"pid:{num}"]
            info = f"开始更新Pixiv搜图UID：\npid:{num}"
        else:
            update_lst = [f"uid:{num}"]
            info = f"开始更新Pixiv搜图UID：\nuid:{num}"
    await start_update.send(info)
    start_time = time.time()
    pid_count, pic_count = await start_update_image_url(update_lst[:num], black_pid)
    await start_update.send(
        f"Pixiv搜图关键词搜图更新完成...\n"
        f"累计更新PID {pid_count} 个\n"
        f"累计更新图片 {pic_count} 张" + "\n耗时：{:.2f}秒".format((time.time() - start_time))
    )


@check_not_update_uid_pid.handle()
async def _(arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    flag = False
    if msg == "update":
        flag = True
    _pass_keyword, _ = await PixivKeywordUser.get_current_keyword()
    x_uid = []
    x_pid = []
    _uid = [int(x[4:]) for x in _pass_keyword if x.startswith("uid:")]
    _pid = [int(x[4:]) for x in _pass_keyword if x.startswith("pid:")]
    all_images = await Pixiv.query_images(r18=2)
    for img in all_images:
        if img.pid not in x_pid:
            x_pid.append(img.pid)
        if img.uid not in x_uid:
            x_uid.append(img.uid)
    await check_not_update_uid_pid.send(
        "从未更新过的UID："
        + "，".join([f"uid:{x}" for x in _uid if x not in x_uid])
        + "\n"
        + "从未更新过的PID："
        + "，".join([f"pid:{x}" for x in _pid if x not in x_pid])
    )
    if flag:
        await check_not_update_uid_pid.send("开始自动自动更新PID....")
        update_lst = [f"pid:{x}" for x in _uid if x not in x_uid]
        black_pid = await PixivKeywordUser.get_black_pid()
        start_time = time.time()
        pid_count, pic_count = await start_update_image_url(update_lst, black_pid)
        await check_not_update_uid_pid.send(
            f"Pixiv搜图关键词搜图更新完成...\n"
            f"累计更新PID {pid_count} 个\n"
            f"累计更新图片 {pic_count} 张" + "\n耗时：{:.2f}秒".format((time.time() - start_time))
        )


@check_omega.handle()
async def _():
    async def _tasks(line: str, all_pid: List[int], length: int, index: int):
        data = line.split("VALUES", maxsplit=1)[-1].strip()
        if data.startswith("("):
            data = data[1:]
        if data.endswith(");"):
            data = data[:-2]
        x = data.split(maxsplit=3)
        pid = int(x[1][:-1].strip())
        if pid in all_pid:
            logger.info(f"添加OmegaPixivIllusts图库数据已存在 ---> pid：{pid}")
            return
        uid = int(x[2][:-1].strip())
        x = x[3].split(", '")
        title = x[0].strip()[1:-1]
        tmp = x[1].split(", ")
        author = tmp[0].strip()[:-1]
        nsfw_tag = int(tmp[1])
        width = int(tmp[2])
        height = int(tmp[3])
        tags = x[2][:-1]
        url = x[3][:-1]
        if await OmegaPixivIllusts.add_image_data(
                pid,
                title,
                width,
                height,
                url,
                uid,
                author,
                nsfw_tag,
                tags,
                datetime.min,
                datetime.min,
        ):
            logger.info(
                f"成功添加OmegaPixivIllusts图库数据 pid：{pid} 本次预计存储 {length} 张，已更新第 {index} 张"
            )
        else:
            logger.info(f"添加OmegaPixivIllusts图库数据已存在 ---> pid：{pid}")
    omega_pixiv_illusts = None
    for file in os.listdir("."):
        if "omega_pixiv_illusts" in file and ".sql" in file:
            omega_pixiv_illusts = Path() / file
    if omega_pixiv_illusts:
        with open(omega_pixiv_illusts, "r", encoding="utf8") as f:
            lines = f.readlines()
        tasks = []
        length = len([x for x in lines if "INSERT INTO" in x.upper()])
        all_pid = await OmegaPixivIllusts.get_all_pid()
        index = 0
        logger.info("检测到OmegaPixivIllusts数据库，准备开始更新....")
        for line in lines:
            if "INSERT INTO" in line.upper():
                index += 1
                tasks.append(
                    asyncio.ensure_future(_tasks(line, all_pid, length, index))
                )
        await asyncio.gather(*tasks)
        omega_pixiv_illusts.unlink()
