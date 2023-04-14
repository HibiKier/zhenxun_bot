import random
from typing import Any, Optional, Tuple, Type

from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    Event,
    GroupMessageEvent,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor
from nonebot.params import CommandArg, RegexGroup
from nonebot.typing import T_State

from configs.config import NICKNAME, Config
from models.sign_group_user import SignGroupUser
from services.log import logger
from utils.depends import OneCommand
from utils.manager import withdraw_message_manager
from utils.message_builder import custom_forward_msg
from utils.utils import is_number

from .._model import Setu
from .data_source import (
    add_data_to_database,
    check_local_exists_or_download,
    gen_message,
    get_luoxiang,
    get_setu_list,
    get_setu_urls,
    search_online_setu,
)

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__zx_plugin_name__ = "色图"
__plugin_usage__ = f"""
usage：
    搜索 lolicon 图库，每日色图time...
    指令：
        色图: 随机本地色图
        色图r: 随机在线十张r18涩图
        色图 [id]: 本地指定id色图
        色图 *[tags]: 在线搜索指定tag色图
        色图r *[tags]: 同上
        [1-9]张涩图: 本地随机色图连发
        [1-9]张[tags]的涩图: 在线搜索指定tag色图连发
        [1-9]张涩图r[tags]: 同上
    示例：色图 萝莉|少女 白丝|黑丝
    示例：色图 萝莉 猫娘
    注：
        tag至多取前20项，| 为或，萝莉|少女=萝莉或者少女
""".strip()
__plugin_des__ = "不要小看涩图啊混蛋！"
__plugin_cmd__ = [
    "色图 ?[id]",
    "色图 ?[tags]",
    "色图r ?[tags]",
    "[1-9]张?[tags]色图",
    "[1-9]张色图?[tags]",
]
__plugin_type__ = ("来点好康的",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 9,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["色图", "涩图", "瑟图"],
}
__plugin_block_limit__ = {}
__plugin_cd_limit__ = {
    "rst": "您冲的太快了，请稍后再冲.",
}
__plugin_configs__ = {
    "WITHDRAW_SETU_MESSAGE": {
        "value": (0, 1),
        "help": "自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        "default_value": (0, 1),
        "type": Tuple[int, int],
    },
    "ONLY_USE_LOCAL_SETU": {
        "value": False,
        "help": "仅仅使用本地色图，不在线搜索",
        "default_value": False,
        "type": bool,
    },
    "INITIAL_SETU_PROBABILITY": {
        "value": 0.7,
        "help": "初始色图概率，总概率 = 初始色图概率 + 好感度",
        "default_value": 0.7,
        "type": float,
    },
    "DOWNLOAD_SETU": {
        "value": True,
        "help": "是否存储下载的色图，使用本地色图可以加快图片发送速度",
        "default_value": True,
        "type": bool,
    },
    "TIMEOUT": {"value": 10, "help": "色图下载超时限制(秒)", "default_value": 10, "type": int},
    "SHOW_INFO": {
        "value": True,
        "help": "是否显示色图的基本信息，如PID等",
        "default_value": True,
        "type": bool,
    },
    "ALLOW_GROUP_R18": {
        "value": False,
        "help": "在群聊中启用R18权限",
        "default_value": False,
        "type": bool,
    },
    "MAX_ONCE_NUM2FORWARD": {
        "value": None,
        "help": "单次发送的图片数量达到指定值时转发为合并消息",
        "default_value": None,
        "type": int,
    },
    "MAX_ONCE_NUM": {
        "value": 10,
        "help": "单次发送图片数量限制",
        "default_value": 10,
        "type": int,
    },
}
Config.add_plugin_config("pixiv", "PIXIV_NGINX_URL", "i.pixiv.re", help_="Pixiv反向代理")

setu_data_list = []


@run_postprocessor
async def _(
    matcher: Matcher,
    exception: Optional[Exception],
    bot: Bot,
    event: Event,
    state: T_State,
):
    global setu_data_list
    if isinstance(event, MessageEvent):
        if matcher.plugin_name == "send_setu":
            # 添加数据至数据库
            try:
                await add_data_to_database(setu_data_list)
                logger.info("色图数据自动存储数据库成功...")
                setu_data_list = []
            except Exception:
                pass


setu = on_command(
    "色图", aliases={"涩图", "不够色", "来一发", "再来点", "色图r"}, priority=5, block=True
)

setu_reg = on_regex("(.*)[份|发|张|个|次|点](.*)[瑟|色|涩]图(r?)(.*)$", priority=5, block=True)


@setu.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
    cmd: str = OneCommand(),
    arg: Message = CommandArg(),
):
    msg = arg.extract_plain_text().strip()
    if isinstance(event, GroupMessageEvent):
        user, _ = await SignGroupUser.get_or_create(
            user_id=str(event.user_id), group_id=str(event.group_id)
        )
        impression = user.impression
        if luox := get_luoxiang(impression):
            await setu.finish(luox)
    r18 = False
    num = 1
    # 是否看r18
    if cmd == "色图r" and isinstance(event, PrivateMessageEvent):
        r18 = True
        num = 10
    elif cmd == "色图r" and isinstance(event, GroupMessageEvent):
        if not Config.get_config("send_setu", "ALLOW_GROUP_R18"):
            await setu.finish(
                random.choice(["这种不好意思的东西怎么可能给这么多人看啦", "羞羞脸！给我滚出克私聊！", "变态变态变态变态大变态！"])
            )
        else:
            r18 = False
    # 有 数字 的话先尝试本地色图id
    if msg and is_number(msg):
        setu_list, code = await get_setu_list(int(msg), r18=r18)
        if code != 200:
            await setu.finish(setu_list[0], at_sender=True)
        setu_img, code = await check_local_exists_or_download(setu_list[0])
        msg_id = await setu.send(gen_message(setu_list[0]) + setu_img, at_sender=True)
        logger.info(
            f"发送色图 {setu_list[0].local_id}.jpg",
            cmd,
            event.user_id,
            getattr(event, "group_id", None),
        )
        if msg_id:
            withdraw_message_manager.withdraw_message(
                event,
                msg_id["message_id"],
                Config.get_config("send_setu", "WITHDRAW_SETU_MESSAGE"),
            )
        return
    await send_setu_handle(bot, setu, event, cmd, msg, num, r18)


num_key = {
    "一": 1,
    "二": 2,
    "两": 2,
    "双": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}


@setu_reg.handle()
async def _(bot: Bot, event: MessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    if isinstance(event, GroupMessageEvent):
        user, _ = await SignGroupUser.get_or_create(
            user_id=str(event.user_id), group_id=str(event.group_id)
        )
        impression = user.impression
        if luox := get_luoxiang(impression):
            await setu.finish(luox, at_sender=True)
    num, tags, r18, tags2 = reg_group
    num = num or "一"
    tags = tags[:-1] if tags and tags[-1] == "的" else tags
    if num_key.get(num):
        num = num_key[num]
    try:
        num = int(num)
    except ValueError:
        num = 1
    if (
        r18
        and not Config.get_config("send_setu", "ALLOW_GROUP_R18")
        and isinstance(event, GroupMessageEvent)
    ):
        await setu.finish(
            random.choice(["这种不好意思的东西怎么可能给这么多人看啦", "羞羞脸！给我滚出克私聊！", "变态变态变态变态大变态！"])
        )
    else:
        limit = Config.get_config("send_setu", "MAX_ONCE_NUM")
        if limit and num > limit:
            num = limit
            await setu.send(f"一次只能给你看 {num} 张哦")
        await send_setu_handle(
            bot, setu_reg, event, "色图r" if r18 else "色图", tags + " " + tags2, num, r18
        )


async def send_setu_handle(
    bot: Bot,
    matcher: Type[Matcher],
    event: MessageEvent,
    command: str,
    msg: str,
    num: int,
    r18: bool,
):
    global setu_data_list
    # 非 id，在线搜索
    tags = msg.split()
    # 真寻的色图？怎么可能
    if f"{NICKNAME}" in tags:
        await matcher.finish("咳咳咳，虽然我很可爱，但是我木有自己的色图~~~有的话记得发我一份呀")
    # 本地先拿图，下载失败补上去
    setu_list, code = None, 200
    setu_count = await Setu.filter(is_r18=r18).count()
    max_once_num2forward = Config.get_config("send_setu", "MAX_ONCE_NUM2FORWARD")
    if (
        not Config.get_config("send_setu", "ONLY_USE_LOCAL_SETU") and tags
    ) or setu_count <= 0:
        # 先尝试获取在线图片
        urls, text_list, add_databases_list, code = await get_setu_urls(
            tags, num, r18, command
        )
        for x in add_databases_list:
            setu_data_list.append(x)
        # 未找到符合的色图，想来本地应该也没有
        if code == 401:
            await setu.finish(urls[0], at_sender=True)
        if code == 200:
            forward_list = []
            for i in range(len(urls)):
                try:
                    msg_id = None
                    setu_img, index = await search_online_setu(urls[i])
                    # 下载成功的话
                    if index != -1:
                        logger.info(
                            f"发送色图 {index}.png",
                            "command",
                            event.user_id,
                            getattr(event, "group_id", None),
                        )
                        if (
                            max_once_num2forward
                            and num >= max_once_num2forward
                            and isinstance(event, GroupMessageEvent)
                        ):
                            forward_list.append(Message(f"{text_list[i]}\n{setu_img}"))
                        else:
                            msg_id = await matcher.send(
                                Message(f"{text_list[i]}\n{setu_img}")
                            )
                    else:
                        if setu_list is None:
                            setu_list, code = await get_setu_list(tags=tags, r18=r18)
                        if code != 200:
                            await setu.finish(setu_list[0], at_sender=True)
                        if setu_list:
                            setu_image = random.choice(setu_list)
                            setu_list.remove(setu_image)
                            if (
                                max_once_num2forward
                                and num >= max_once_num2forward
                                and isinstance(event, GroupMessageEvent)
                            ):
                                forward_list.append(
                                    gen_message(setu_image)
                                    + (
                                        await check_local_exists_or_download(setu_image)
                                    )[0]
                                )
                            else:
                                msg_id = await matcher.send(
                                    gen_message(setu_image)
                                    + (
                                        await check_local_exists_or_download(setu_image)
                                    )[0]
                                )
                            logger.info(
                                f"发送本地色图 {setu_image.local_id}.png",
                                "command",
                                event.user_id,
                                getattr(event, "group_id", None),
                            )
                        else:
                            msg_id = await matcher.send(text_list[i] + "\n" + setu_img)
                    if msg_id:
                        withdraw_message_manager.withdraw_message(
                            event,
                            msg_id["message_id"],
                            Config.get_config("send_setu", "WITHDRAW_SETU_MESSAGE"),
                        )
                except ActionFailed:
                    await matcher.finish("坏了，这张图色过头了，我自己看看就行了！", at_sender=True)
            if forward_list and isinstance(event, GroupMessageEvent):
                msg_id = await bot.send_group_forward_msg(
                    group_id=event.group_id,
                    messages=custom_forward_msg(forward_list, bot.self_id),
                )
                withdraw_message_manager.withdraw_message(
                    event,
                    msg_id,
                    Config.get_config("send_setu", "WITHDRAW_SETU_MESSAGE"),
                )
            return
    if code != 200:
        await matcher.finish("网络连接失败...", at_sender=True)
    # 本地无图
    if setu_list is None:
        setu_list, code = await get_setu_list(tags=tags, r18=r18)
        if code != 200:
            await matcher.finish(setu_list[0], at_sender=True)
    # 开始发图
    forward_list = []
    for _ in range(num):
        if not setu_list:
            await setu.finish("坏了，已经没图了，被榨干了！")
        setu_image = random.choice(setu_list)
        setu_list.remove(setu_image)
        if (
            max_once_num2forward
            and num >= max_once_num2forward
            and isinstance(event, GroupMessageEvent)
        ):
            forward_list.append(
                Message(
                    gen_message(setu_image)
                    + (await check_local_exists_or_download(setu_image))[0]
                )
            )
        else:
            try:
                msg_id = await matcher.send(
                    gen_message(setu_image)
                    + (await check_local_exists_or_download(setu_image))[0]
                )
                withdraw_message_manager.withdraw_message(
                    event,
                    msg_id["message_id"],
                    Config.get_config("send_setu", "WITHDRAW_SETU_MESSAGE"),
                )
                logger.info(
                    f"发送本地色图 {setu_image.local_id}.png",
                    "command",
                    event.user_id,
                    getattr(event, "group_id", None),
                )
            except ActionFailed:
                await matcher.finish("坏了，这张图色过头了，我自己看看就行了！", at_sender=True)
    if forward_list and isinstance(event, GroupMessageEvent):
        msg_id = await bot.send_group_forward_msg(
            group_id=event.group_id,
            messages=custom_forward_msg(forward_list, bot.self_id),
        )
        withdraw_message_manager.withdraw_message(
            event, msg_id, Config.get_config("send_setu", "WITHDRAW_SETU_MESSAGE")
        )
