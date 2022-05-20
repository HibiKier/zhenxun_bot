from json import load
from pathlib import Path

from nonebot import get_driver
from nonebot.log import logger

from configs.config import Config
from .models import SetuMessage

if Config.get_config("nonebot_plugin_setu_now", "SETU_SEND_CUSTOM_MESSAGE_PATH"):
    MSG_PATH = Path(str(Config.get_config("nonebot_plugin_setu_now", "SETU_SEND_CUSTOM_MESSAGE_PATH"))).absolute()
else:
    MSG_PATH = None


DEFAULT_MSG = {
    "send": [
        "给大佬递图",
        "这是你的🐍图",
        "你是大色批",
        "看！要色图的色批出现了！",
        "？",
        "喏，图",
        "给给给个🐍图",
        "色图有我好冲吗？",
        "呐呐呐，欧尼酱别看色图了呐",
        "有什么好色图有给发出来让大伙看看！",
        "没有，有也不给（骗你的～）",
        "天天色图色图的，今天就把你变成色图！",
        "咱没有色图（骗你的～）",
        "哈？你的脑子一天都在想些什么呢，咱才没有这种东西啦。",
        "呀！不要啊！等一...下~",
        "呜...不要啦！太色了咱~",
        "不要这样子啦(*/ω＼*)",
        "Hen....Hentai！。",
        "讨....讨厌了（脸红）",
        "你想...想做什么///",
        "啊.....你...你要干什么？！走开.....走开啦大hentai！一巴掌拍飞！(╯‵□′)╯︵┻━┻",
        "变态baka死宅？",
        "已经可以了，现在很多死宅也都没你这么恶心了",
        "噫…你这个死变态想干嘛！居然想叫咱做这种事，死宅真恶心！快离我远点，我怕你污染到周围空气了（嫌弃脸）",
        "这么喜欢色图呢？不如来点岛风色图？",
        "hso！",
        "这么喜欢看色图哦？变态？",
        "eee，死肥宅不要啦！恶心心！",
    ],
    "cd": [
        "憋冲了！你已经冲不出来了{cd_msg}后可以再次发送哦！",
        "憋住，不准冲！CD:{cd_msg}",
        "你的色图不出来了！还需要{cd_msg}才能出来哦",
        "注意身体，色图看太多对身体不好 (╯‵□′)╯︵┻━┻ 你还需要{cd_msg}才能再次发送哦",
        "憋再冲了！{cd_msg}",
        "呃...好像冲了好多次...感觉不太好呢...{cd_msg}后再冲吧",
        "？？？",
        "你急啥呢？",
        "你这么喜欢色图，{cd_msg}后再给你看哦",
    ],
}


def load_setu_message():
    if MSG_PATH:
        logger.info(f"加载自定义色图消息 路径: {MSG_PATH}")
        with MSG_PATH.open("r") as f:
            msg = load(f)
        return SetuMessage(**msg)
    else:
        return SetuMessage(**DEFAULT_MSG)


SETU_MSG: SetuMessage = load_setu_message()
