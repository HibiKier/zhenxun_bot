import random
from nonebot import on_command, on_regex
from services.log import logger
from models.sign_group_user import SignGroupUser
from nonebot.message import run_postprocessor
from nonebot.matcher import Matcher
from typing import Optional, Type, Any
from gino.exceptions import UninitializedError

from utils.message_builder import custom_forward_msg
from utils.utils import (
    is_number,
)
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    Bot,
    ActionFailed,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    Message,
    Event,
)
from plugins.sign_in import utils
from .data_source import (
    get_setu_list,
    get_luoxiang,
    search_online_setu,
    get_setu_urls,
    find_img_index,
    gen_message,
    check_local_exists_or_download,
    add_data_to_database,
    get_setu_count,
)
from typing import List
from nonebot.adapters.onebot.v11.exception import ActionFailed
from configs.config import Config, NICKNAME
from utils.manager import withdraw_message_manager
from nonebot.params import CommandArg, Command, RegexGroup
from typing import Tuple
import re
from utils.message_builder import image
from .._model import Setu
from utils.message_builder import custom_forward_msg

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
        [1-9]张[tags]的涩图: 指定tag色图连发
    示例：色图 萝莉|少女 白丝|黑丝
    示例：色图 萝莉 猫娘
    注：
        tag至多取前20项，| 为或，萝莉|少女=萝莉或者少女
""".strip()
__plugin_des__ = "不要小看涩图啊混蛋！"
__plugin_cmd__ = ["色图 ?[id]", "色图 ?[tags]", "色图r ?[tags]", "[1-9]张?[tags]色图"]
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
    },
    "ONLY_USE_LOCAL_SETU": {
        "value": False,
        "help": "仅仅使用本地色图，不在线搜索",
        "default_value": False,
    },
    "INITIAL_SETU_PROBABILITY": {
        "value": 0.7,
        "help": "初始色图概率，总概率 = 初始色图概率 + 好感度",
        "default_value": 0.7,
    },
    "DOWNLOAD_SETU": {
        "value": True,
        "help": "是否存储下载的色图，使用本地色图可以加快图片发送速度",
        "default_value": True,
    },
    "HASH_OBFUSCATION": {
        "value": False,
        "help": "是否混淆图片hash，可能解决图片被风控，发不出的情况，但会占用更多系统资源并减慢发送速度",
        "default_value": False,
    },
    "ALLOW_R18": {
        "value": False,
        "help": "是否允许R18，关闭后无论私聊或者群组都不能发R18",
        "default_value": False,
    },
    "TIMEOUT": {"value": 10, "help": "色图下载超时限制(秒)", "default_value": 10},
    "SHOW_INFO": {"value": True, "help": "是否显示色图的基本信息，如PID等", "default_value": True},
    "ALLOW_GROUP_R18": {"value": False, "help": "在群聊中启用R18权限", "default_value": False},
    "MAX_ONCE_NUM2FORWARD": {
        "value": None,
        "help": "单次发送的图片数量达到指定值时转发为合并消息",
        "default_value": None,
    },
}
Config.add_plugin_config("pixiv", "PIXIV_NGINX_URL", "i.pixiv.re", help_="Pixiv反向代理")

setu_data_list = []
NICKNAMES = ["格蕾修", "小格蕾修", "格雷修", "小格雷修", "griseo"]


@run_postprocessor
async def do_something(
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
            except UninitializedError:
                pass


setu = on_command(
    "色图", aliases={"涩图", "不够色", "来一发", "再来点", "色图r"}, priority=8, block=True
)

setu_reg = on_regex("(.*)[份|发|张|个|次|点](.*)[瑟|色|涩]图$", priority=8, block=True)


@setu.handle()

async def _(
    bot: Bot,
    event: MessageEvent,
    cmd: Tuple[str, ...] = Command(),
    arg: Message = CommandArg(),
):
    msg = arg.extract_plain_text().strip()

    if isinstance(event, GroupMessageEvent):
        impression = (
            await SignGroupUser.ensure(event.user_id, event.group_id)
        ).impression
        luox = get_luoxiang(impression)
        if luox:
            await setu.finish(luox)
    r18 = 0
    num = 1
    # 是否看r18
    if cmd[0] == "色图r" and not Config.get_config("send_setu", "ALLOW_R18"):
        await setu.finish(
            random.choice(["这种不好意思的东西怎么可能给这么多人看啦", "变态变态变态变态大变态！"]),
            at_sender=True if isinstance(event, GroupMessageEvent) else False
        )
    if cmd[0] == "色图r" and isinstance(event, PrivateMessageEvent):
        r18 = 1
        num = 10
    elif cmd[0] == "色图r" and isinstance(event, GroupMessageEvent):
        if not Config.get_config("send_setu", "ALLOW_GROUP_R18"):
            await setu.finish(
                random.choice(["这种不好意思的东西怎么可能给这么多人看啦", "羞羞脸！给我滚出克私聊！", "变态变态变态变态大变态！"]),
                at_sender=True if isinstance(event, GroupMessageEvent) else False
            )
        else:
            r18 = 1

    # 有 数字 的话先尝试本地色图id
    if msg and is_number(msg):
        setu_list, code = await get_setu_list(int(msg), r18=r18)
        if code != 200:
            await setu.finish(setu_list[0], at_sender=True if isinstance(event, GroupMessageEvent) else False)

        setu_img, code = await check_local_exists_or_download(setu_list[0])
        msg_id = await setu.send(await gen_message(setu_list[0]) + setu_img,
                                 at_sender=True if isinstance(event, GroupMessageEvent) else False)

        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 发送色图 {setu_list[0].local_id}.jpg"
        )
        if msg_id:
            withdraw_message_manager.withdraw_message(
                event,
                msg_id["message_id"],
                Config.get_config("send_setu", "WITHDRAW_SETU_MESSAGE"),
            )
        return
    await send_setu_handle(bot, setu, event, cmd[0], msg, num, r18)


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
        impression = (
            await SignGroupUser.ensure(event.user_id, event.group_id)
        ).impression
        luox = get_luoxiang(impression)
        if luox:
            await setu.finish(luox, at_sender=True)
    num, tags = reg_group
    num = num or 1
    tags = tags[:-1] if tags and tags[-1] == "的" else tags
    if num_key.get(num):
        num = num_key[num]
    try:
        num = int(num)
    except ValueError:
        num = 1
    await send_setu_handle(bot, setu_reg, event, "色图", tags, num, 0)


async def send_setu_handle(
    bot: Bot,
    matcher: Type[Matcher],
    event: MessageEvent,
    command: str,
    msg: str,
    num: int,
    r18: int,
):
    count = 0
    global setu_data_list
    # 非 id，在线搜索
    tags = msg.split()
    # 格蕾修的色图？怎么可能
    tags = [x.lower() for x in tags]
    test = [l for l in NICKNAMES if l in tags]
    if num > 10:
        await matcher.finish(f"你也太贪心了吧",
                             at_sender=True if isinstance(event, GroupMessageEvent) else False)
    if isinstance(event, GroupMessageEvent):
        impression = (
            await SignGroupUser.ensure(event.user_id, event.group_id)
        ).impression
        level, next_impression, previous_impression = utils.get_level_and_next_impression(
            impression
        )
        if test and int(level) < 4:
            await matcher.finish(image("0", "griseo"), at_sender=True)
    # 本地先拿图，下载失败补上
    setu_list = []
    if num > 1:
        setu_list = await Setu.query_image(None, tags, r18, hash_not_none=True)
    if len(setu_list) < num or num == 1:
        setu_list, code = [], 200
        # setu_count = await get_setu_count(r18)
        if not Config.get_config("send_setu", "ONLY_USE_LOCAL_SETU"):
            # 先尝试获取在线图片
            urls, text_list, add_databases_list, code = await get_setu_urls(
                tags, num, r18, command
            )
            for x in add_databases_list:
                setu_data_list.append(x)
            if code == 401:
                # 尝试本地找图
                setu_list = await Setu.query_image(None, tags, r18, hash_not_none=True)
                if len(setu_list) == 0:
                    logger.info("没找到符合条件的色图...")
                    await setu.finish(urls[0], at_sender=True if isinstance(event, GroupMessageEvent) else False)
                else:
                    code = 301
            if code == 200:
                for i in range(len(urls)):
                    setu_list1 = await Setu.query_image(img_url=urls[i], hash_not_none=True)
                    if len(setu_list1) != 0:
                        if setu_list1[0] not in setu_list:
                            setu_list.append(setu_list1[0])

                    else:
                        try:
                            setu_img, index = await search_online_setu(urls[i])
                            # 下载成功的话
                            if index != -1:
                                logger.info(
                                    f"(USER {event.user_id}, GROUP "
                                    f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                                    f" 发送色图 {index}.jpg"
                                )
                                msg_id = await matcher.send(
                                    Message(f"{text_list[i]}\n{setu_img}"
                                            ), at_sender=True if isinstance(event, GroupMessageEvent) else False
                                )
                                count += 1
                            else:
                                if len(setu_list) == 0:
                                    logger.info(f"没找到符合条件的色图...")
                                    await matcher.finish(f"没找到符合条件的色图...",
                                                         at_sender=True if isinstance(event,
                                                                                      GroupMessageEvent) else False)
                            if msg_id:
                                withdraw_message_manager.withdraw_message(
                                    event,
                                    msg_id["message_id"],
                                    Config.get_config("send_setu", "WITHDRAW_SETU_MESSAGE"),
                                )
                        except ActionFailed:
                            await matcher.finish("坏了，这张图色过头了，我自己看看就行了！",
                                                 at_sender=True if isinstance(event, GroupMessageEvent) else False)
        if code != 200 and code != 301:
            await matcher.finish(f"网络连接失败..." + image("1", "griseo"),
                                 at_sender=True if isinstance(event, GroupMessageEvent) else False)
        # 开始发图
    # 本地无图
    # if len(setu_list) == 0:
    #     # setu_list, code = await get_setu_list(tags=tags, r18=r18)
    #     # if code != 200:
    #     logger.info(f"没找到符合条件的色图...2")
    #     await matcher.finish(f"没找到符合条件的色图...", at_sender=True if isinstance(event, GroupMessageEvent) else False)
    failure_msg: int = 0
    if count < num:
        if isinstance(event, PrivateMessageEvent) or num <= 3 and len(setu_list) > 0:
            for _ in range(num):
                if not setu_list:
                    await setu.finish("坏了，已经没图了，被榨干了！")
                setu_image = random.choice(setu_list)
                setu_list.remove(setu_image)
                try:
                    msg1 = await gen_message(setu_image, True, msg)
                    msg_id = await matcher.send(
                        Message(msg1)
                        , at_sender=True if isinstance(event, GroupMessageEvent) else False
                    )
                    withdraw_message_manager.withdraw_message(
                        event,
                        msg_id["message_id"],
                        Config.get_config("send_setu", "WITHDRAW_SETU_MESSAGE"),
                    )
                    logger.info(
                        f"(USER {event.user_id}, GROUP "
                        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                        f" 发送本地色图 {setu_image.local_id}.jpg"
                    )
                except Exception as e:
                    logger.error(e)
                    failure_msg += 1

        elif isinstance(event, GroupMessageEvent) and len(setu_list) > 0:
            await matcher.send("数据量较大,正在处理", at_sender=True)
            use_list = []
            num_local = num
            if len(setu_list) >= num:
                while num_local > 0:
                    setu_image = random.choice(setu_list)
                    setu_list.remove(setu_image)
                    num_local -= 1
                    use_list.append(setu_image)
                message_list = [Message(
                    await gen_message(i, True, msg)
                ) for i in use_list]
            else:
                message_list = [Message(
                    await gen_message(i, True, msg)
                ) for i in setu_list]
            try:
                await bot.send_group_forward_msg(
                    group_id=event.group_id, messages=custom_forward_msg(message_list, bot.self_id)
                )
            except Exception as e:
                logger.error(e)
                failure_msg = num
        if failure_msg >= num / 2:
            await matcher.finish("坏了，这张图色过头了，我自己看看就行了！" + image("1", "griseo"),
                                 at_sender=True if isinstance(event, GroupMessageEvent) else False)
