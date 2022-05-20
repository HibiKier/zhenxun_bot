from re import I, sub
from typing import List
from asyncio import sleep

from nonebot import on_regex, get_driver
from nonebot.log import logger
from nonebot.params import State
from nonebot.typing import T_State
from nonebot.exception import ActionFailed
from nonebot.adapters.onebot.v11 import (
    GROUP,
    PRIVATE_FRIEND,
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
    GroupMessageEvent,
    PrivateMessageEvent,
)

from .utils import send_forward_msg
from configs.config import NICKNAME, Config
from .models import Setu, SetuNotFindError
from .withdraw import add_withdraw_job
from .cd_manager import add_cd, cd_msg, check_cd, remove_cd
from .data_source import SetuLoader



__zx_plugin_name__ = "色图1"
__plugin_usage__ = """
usage：
    - 指令 以 `setu|色图|涩图|来点色色|色色|涩涩` 为开始
  - 然后接上可选数量 `x10` `10张|个|份`
  - 再接上可选 `r18`
  - 可选 `tag`
  - 最后是关键词
- 说明
  - 数量 可选 默认为 1
  - `r18` 可选 仅在私聊可用 群聊直接忽视
  - `tag` 可选 如有 关键词参数会匹配 `pixiv 标签 tag`
  - 关键词 可选 匹配任何 `标题` `作者` 或 `pixiv 标签`
- 例子
  - `来点色色 妹妹`
  - `setur18`
  - `色图 x20 tag 碧蓝航线 妹妹`
  - `涩涩10份魅魔`
""".strip()
__plugin_des__ = "色图1"
__plugin_type__ = ("来点好康的",)
__plugin_cmd__ = ["色图", "来点色色", "setu", "色图10份魅魔"]
__plugin_version__ = 0.1
__plugin_author__ = "kexue-z"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": [
        "色图", "涩图", "瑟图"
    ],
}
__plugin_cd_limit__ = {
    "rst": "您冲的太快了，请稍后再冲.",
}
__plugin_configs__ = {
    "SETU_CD": {
        "value": 60,
        "help": "触发CD(单位秒) 可选 默认60秒",
        "default_value": 60,
    },
    "SETU_SAVE": {
        "value": None,
        "help": "保存模式 可选 webdav(保存到 webdav 服务器中) 或 local(本地) 或 留空,不保存",
        "default_value": None,
    },
    "SETU_PATH": {
        "value": None,
        "help": "保存模式 可选 webdav(保存到 webdav 服务器中) 或 local(本地) 或 留空,不保存",
        "default_value": None,
    },
    "SETU_PROXY": {
        "value": None,
        "help": "代理地址 可选 当 pixiv 反向代理不能使用时可自定义",
        "default_value": None,
    },
    "SETU_REVERSE_PROXY": {
        "value": "i.pixiv.re",
        "help": "pixiv 反向代理 可选 默认 i.pixiv.re",
        "default_value": "i.pixiv.re",
    },
    "SETU_DAV_URL": {
        "value": None,
        "help": "webdav 服务器地址",
        "default_value": None,
    },
    "SETU_DAV_USERNAME": {
        "value": None,
        "help": "webdav 用户名",
        "default_value": None,
    },
    "SETU_DAV_PASSWORD": {
        "value": None,
        "help": "webdav 密码",
        "default_value": None,
    },
    "SETU_SEND_INFO_MESSAGE": {
        "value": True,
        "help": "是否发送图片信息 可选 默认 ture 填写 false 可关闭",
        "default_value": True,
    },
    "SETU_SEND_CUSTOM_MESSAGE_PATH": {
        "value": None,
        "help": "自定义发送消息路径 可选 当填写路径时候开启 可以为相对路径",
        "default_value": None,
    },
    "SETU_WITHDRAW": {
        "value": None,
        "help": "撤回发送的色图消息的时间, 单位: 秒 可选 默认关闭 填入数字来启用, 建议 10 ~ 120 仅对于非合并转发使用",
        "default_value": None,
    },
    "SETU_SIZE": {
        "value": "regular",
        "help": "色图质量 默认 regular 可选 original regular small thumb mini",
        "default_value": "regular",
    },
    "SETU_API_URL": {
        "value": "https://api.lolicon.app/setu/v2",
        "help": "色图信息 api 地址 默认https://api.lolicon.app/setu/v2 如果有 api 符合类型也能用",
        "default_value": "https://api.lolicon.app/setu/v2",
    },
    "SETU_MAX": {
        "value": 3,
        "help": "一次获取色图的数量 默认 30 如果你的服务器/主机内存吃紧 建议调小",
        "default_value": 3,
    },
    "INITIAL_SETU_PROBABILITY": {
        "value": 0.7,
        "help": "初始色图概率，总概率 = 初始色图概率 + 好感度",
        "default_value": 0.7,
    },
}
SAVE = Config.get_config("nonebot_plugin_setu_now", "SETU_SAVE")
SETU_SIZE = Config.get_config("nonebot_plugin_setu_now", "SETU_SIZE")
MAX = Config.get_config("nonebot_plugin_setu_now", "SETU_MAX")
if SAVE == "webdav":
    from .save_to_webdav import save_img
elif SAVE == "local":
    from .save_to_local import save_img

setu_matcher = on_regex(
    r"^(setu|色图|涩图|来点色色|色色|涩涩|来点色图)\s?([x|✖️|×|X|*]?\d+[张|个|份]?)?\s?(r18)?\s?\s?(tag)?\s?(.*)?",
    flags=I,
    permission=PRIVATE_FRIEND | GROUP,
)


@setu_matcher.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State()):
    args = list(state["_matched_groups"])
    num = args[1]
    r18 = args[2]
    tags = args[3]
    key = args[4]

    num = int(sub(r"[张|个|份|x|✖️|×|X|*]", "", num)) if num else 1
    if num > MAX:
        num = MAX

    # 如果存在 tag 关键字, 则将 key 视为tag
    if tags:
        tags = key.split()
        key = ""

    # 仅在私聊中开启
    r18 = True if (isinstance(event, PrivateMessageEvent) and r18) else False

    if cd := check_cd(event):
        # 如果 CD 还没到 则直接结束
        await setu_matcher.finish(cd_msg(cd), at_sender=True)

    logger.debug(f"Setu: r18:{r18}, tag:{tags}, key:{key}, num:{num}")
    add_cd(event, num)

    setu_obj = SetuLoader()
    try:
        data = await setu_obj.get_setu(key, tags, r18, num)
    except SetuNotFindError:
        remove_cd(event)
        await setu_matcher.finish(f"没有找到关于 {tags or key} 的色图呢～", at_sender=True)

    failure_msg: int = 0
    msg_list: List[Message] = []

    for setu in data:
        msg = Message(MessageSegment.image(setu.img))  # type: ignore

        if Config.get_config("nonebot_plugin_setu_now", "SETU_SEND_INFO_MESSAGE"):
            msg.append(MessageSegment.text(setu.msg))  # type: ignore

        msg_list.append(msg)  # type: ignore

        if SAVE:
            await save_img(setu)

        # 私聊 或者 群聊中 <= 3 图, 直接发送
    if isinstance(event, PrivateMessageEvent) or len(data) <= 3:
        for msg in msg_list:
            try:
                msg_info = await setu_matcher.send(msg, at_sender=True)
                add_withdraw_job(bot, **msg_info)
                await sleep(2)

            except ActionFailed as e:
                logger.warning(e)
                failure_msg += 1

    # 群聊中 > 3 图, 合并转发
    elif isinstance(event, GroupMessageEvent):

        try:
            await send_forward_msg(bot, event, "好东西", bot.self_id, msg_list)
        except ActionFailed as e:
            logger.warning(e)
            failure_msg = num

    if failure_msg >= num / 2:
        remove_cd(event)

        await setu_matcher.finish(
            message=Message(f"消息被风控，{failure_msg} 个图发不出来了\n"),
            at_sender=True,
        )
