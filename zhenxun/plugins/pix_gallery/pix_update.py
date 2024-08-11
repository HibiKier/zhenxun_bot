import asyncio
import os
import re
import time
from pathlib import Path

from nonebot.adapters import Bot
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Match,
    Option,
    on_alconna,
    store_true,
)
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils

from ._data_source import start_update_image_url
from ._model.omega_pixiv_illusts import OmegaPixivIllusts
from ._model.pixiv import Pixiv
from ._model.pixiv_keyword_user import PixivKeywordUser

__plugin_meta__ = PluginMetadata(
    name="pix检查更新",
    description="pix图库收录数据检查更新",
    usage="""
    指令：
        更新pix关键词 *[keyword/uid/pid] [num=max]: 更新仅keyword/uid/pid或全部
        pix检测更新：检测从未更新过的uid和pid
        示例：更新pix关键词keyword
        示例：更新pix关键词uid 10
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier", version="0.1", plugin_type=PluginType.SUPERUSER
    ).dict(),
)


_update_matcher = on_alconna(
    Alconna("更新pix关键词", Args["type", ["uid", "pid", "keyword"]]["num?", int]),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

_check_matcher = on_alconna(
    Alconna(
        "pix检测更新", Option("-u|--update", action=store_true, help_text="是否更新")
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

_omega_matcher = on_alconna(
    Alconna("检测omega图库"), permission=SUPERUSER, priority=1, block=True
)


@_update_matcher.handle()
async def _(arparma: Arparma, session: EventSession, type: str, num: Match[int]):
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
    _num = num.result if num.available else 9999
    if _num < 10000:
        keyword_str = "，".join(
            _keyword[: _num if _num < len(_keyword) else len(_keyword)]
        )
        uid_str = "，".join(_uid[: _num if _num < len(_uid) else len(_uid)])
        pid_str = "，".join(_pid[: _num if _num < len(_pid) else len(_pid)])
        if type == "pid":
            update_lst = _pid
            info = f"开始更新Pixiv搜图PID：\n{pid_str}"
        elif type == "uid":
            update_lst = _uid
            info = f"开始更新Pixiv搜图UID：\n{uid_str}"
        elif type == "keyword":
            update_lst = _keyword
            info = f"开始更新Pixiv搜图关键词：\n{keyword_str}"
        else:
            update_lst = _pass_keyword
            info = f"开始更新Pixiv搜图关键词：\n{keyword_str}\n更新UID：{uid_str}\n更新PID：{pid_str}"
        _num = _num if _num < len(update_lst) else len(update_lst)
    else:
        if type == "pid":
            update_lst = [f"pid:{_num}"]
            info = f"开始更新Pixiv搜图UID：\npid:{_num}"
        else:
            update_lst = [f"uid:{_num}"]
            info = f"开始更新Pixiv搜图UID：\nuid:{_num}"
    await MessageUtils.build_message(info).send()
    start_time = time.time()
    pid_count, pic_count = await start_update_image_url(
        update_lst[:_num], black_pid, type == "pid"
    )
    await MessageUtils.build_message(
        f"Pixiv搜图关键词搜图更新完成...\n"
        f"累计更新PID {pid_count} 个\n"
        f"累计更新图片 {pic_count} 张"
        + "\n耗时：{:.2f}秒".format((time.time() - start_time))
    ).send()
    logger.info("更新pix关键词", arparma.header_result, session=session)


@_check_matcher.handle()
async def _(bot: Bot, arparma: Arparma, session: EventSession):
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
    await MessageUtils.build_message(
        "从未更新过的UID："
        + "，".join([f"uid:{x}" for x in _uid if x not in x_uid])
        + "\n"
        + "从未更新过的PID："
        + "，".join([f"pid:{x}" for x in _pid if x not in x_pid])
    ).send()
    if arparma.find("update"):
        await MessageUtils.build_message("开始自动自动更新PID....").send()
        update_lst = [f"pid:{x}" for x in _uid if x not in x_uid]
        black_pid = await PixivKeywordUser.get_black_pid()
        start_time = time.time()
        pid_count, pic_count = await start_update_image_url(
            update_lst, black_pid, False
        )
        await MessageUtils.build_message(
            f"Pixiv搜图关键词搜图更新完成...\n"
            f"累计更新PID {pid_count} 个\n"
            f"累计更新图片 {pic_count} 张"
            + "\n耗时：{:.2f}秒".format((time.time() - start_time))
        ).send()
        logger.info(
            f"pix检测更新, 是否更新: {arparma.find('update')}",
            arparma.header_result,
            session=session,
        )


@_omega_matcher.handle()
async def _():
    async def _tasks(line: str, all_pid: list[int], length: int, index: int):
        data = line.split("VALUES", maxsplit=1)[-1].strip()[1:-2]
        num_list = re.findall(r"(\d+)", data)
        pid = int(num_list[1])
        uid = int(num_list[2])
        id_ = 3
        while num_list[id_] not in ["0", "1"]:
            id_ += 1
        classified = int(num_list[id_])
        nsfw_tag = int(num_list[id_ + 1])
        width = int(num_list[id_ + 2])
        height = int(num_list[id_ + 3])
        str_list = re.findall(r"'(.*?)',", data)
        title = str_list[0]
        uname = str_list[1]
        tags = str_list[2]
        url = str_list[3]
        if pid in all_pid:
            logger.info(f"添加OmegaPixivIllusts图库数据已存在 ---> pid：{pid}")
            return
        _, is_create = await OmegaPixivIllusts.get_or_create(
            pid=pid,
            title=title,
            width=width,
            height=height,
            url=url,
            uid=uid,
            nsfw_tag=nsfw_tag,
            tags=tags,
            uname=uname,
            classified=classified,
        )
        if is_create:
            logger.info(
                f"成功添加OmegaPixivIllusts图库数据 pid：{pid} 本次预计存储 {length} 张，已更新第 {index} 张"
            )
        else:
            logger.info(f"添加OmegaPixivIllusts图库数据已存在 ---> pid：{pid}")

    omega_pixiv_illusts = None
    for file in os.listdir("."):
        if "omega_pixiv_artwork" in file and ".sql" in file:
            omega_pixiv_illusts = Path() / file
    if omega_pixiv_illusts:
        with open(omega_pixiv_illusts, "r", encoding="utf8") as f:
            lines = f.readlines()
        tasks = []
        length = len([x for x in lines if "INSERT INTO" in x.upper()])
        all_pid = await OmegaPixivIllusts.all().values_list("pid", flat=True)
        index = 0
        logger.info("检测到OmegaPixivIllusts数据库，准备开始更新....")
        for line in lines:
            if "INSERT INTO" in line.upper():
                index += 1
                logger.info(f"line: {line} 加入更新计划")
                tasks.append(
                    asyncio.create_task(_tasks(line, all_pid, length, index))  # type: ignore
                )
        await asyncio.gather(*tasks)
        omega_pixiv_illusts.unlink()
