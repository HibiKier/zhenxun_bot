from nonebot import on_command, on_regex
from services.log import logger
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message, Bot
from nonebot.typing import T_State
from nonebot.params import CommandArg

from utils.message_builder import image
from utils.utils import get_message_img
from nonebot.internal.params import ArgStr, Arg
from .data_source import get_setu_score

__zx_plugin_name__ = "色图打分"
__plugin_usage__ = """
usage：
    色图打分
    指令：
        色图评分 [图片]
""".strip()
__plugin_des__ = "让我看看你的图色不色"
__plugin_cmd__ = [
    "色图评分",
    "色图打分",
    "涩图评分",
    "涩图打分"
]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 0.1
__plugin_author__ = "HMScygnet"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["色图评分", "色图打分", "涩图评分", "涩图打分"],
}
__plugin_configs__ = {
    "API_KEY": {
        "value": None,
        "help": "百度内容审核的API_KEY，通过 https://cloud.baidu.com/product/imagecensoring 注册获取",
    },
    "SECRET_KEY": {
        "value": None,
        "help": "百度内容审核的SECRET_KEY，通过 https://cloud.baidu.com/product/imagecensoring 注册获取",
    },
}
__plugin_block_limit__ = {
    "rst": "正在评分中……",  # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
}
__plugin_count_limit__ = {
    "max_count": 1,  # 每日次数限制数量
    "rst": "今日已无可调用次数",  # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
}
__plugin_cd_limit__ = {
    "cd": 60,  # 限制 cd 时长
    "rst": "你冲太快了，一会再试吧",  # 回复的话，为None时不回复，可以添加[at]，[uname]，[nickname]来对应艾特，用户群名称，昵称系统昵称
}

setu_score = on_regex("[瑟|色|涩]图[评|打]分", block=True, priority=5)


@setu_score.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, args: Message = CommandArg()):
    img_url = get_message_img(event.json())
    if img_url:
        state["img_url"] = args


@setu_score.got("img_url", prompt="图来")
async def _(bot: Bot, event: MessageEvent, state: T_State, img_url: Message = Arg("img_url")):
    img_url = get_message_img(img_url)
    if not img_url:
        await setu_score.reject_arg("img_url", "发送的必须是图片！")
    img_url = img_url[0]
    await setu_score.send("开始评分.....")
    score, code = await get_setu_score(img_url)
    if code == 200:
        await setu_score.send(image(img_url)+f"色图评分:{score}", at_sender=True)
        logger.info(
            f"USER {event.user_id} GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'}"
            f" 色图评分 {img_url} --> {score}"
        )
    else:
        logger.warning(
            f"USER {event.user_id} GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} 色图评分 {img_url} 错误"
        )
        await setu_score.send(f"{score}"+image("1", "griseo"), at_sender=True)
