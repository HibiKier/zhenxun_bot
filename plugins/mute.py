from nonebot import on_message, on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.adapters.onebot.v11.permission import GROUP
from utils.utils import is_number, get_message_img
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11.exception import ActionFailed
from configs.path_config import DATA_PATH, TEMP_PATH
from utils.image_utils import get_img_hash
from services.log import logger
from configs.config import NICKNAME, Config
from utils.http_utils import AsyncHttpx
from nonebot.params import CommandArg, Command
from typing import Tuple
import time

try:
    import ujson as json
except ModuleNotFoundError:
    import json


__zx_plugin_name__ = "刷屏禁言 [Admin]"
__plugin_usage__ = f"""
usage：
    刷屏禁言相关操作，需要 {NICKNAME} 有群管理员权限
    指令：
        设置刷屏检测时间 [秒]
        设置刷屏检测次数 [次数]
        设置刷屏禁言时长 [分钟]
        刷屏检测设置: 查看当前的刷屏检测设置
        * 即 X 秒内发送同样消息 N 次，禁言 M 分钟 *
""".strip()
__plugin_des__ = "刷屏禁言相关操作"
__plugin_cmd__ = ["设置刷屏检测时间 [秒]", "设置刷屏检测次数 [次数]", "设置刷屏禁言时长 [分钟]", "刷屏检测设置"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {"admin_level": Config.get_config("mute", "MUTE_LEVEL")}
__plugin_configs__ = {
    "MUTE_LEVEL [LEVEL]": {"value": 5, "help": "更改禁言设置的管理权限", "default_value": 5},
    "MUTE_DEFAULT_COUNT": {"value": 10, "help": "刷屏禁言默认检测次数", "default_value": 10},
    "MUTE_DEFAULT_TIME": {"value": 7, "help": "刷屏检测默认规定时间", "default_value": 7},
    "MUTE_DEFAULT_DURATION": {
        "value": 10,
        "help": "刷屏检测默禁言时长（分钟）",
        "default_value": 10,
    },
}


mute = on_message(priority=1, block=False)
mute_setting = on_command(
    "mute_setting",
    aliases={"设置刷屏检测时间", "设置刷屏检测次数", "设置刷屏禁言时长", "刷屏检测设置"},
    permission=GROUP,
    block=True,
    priority=5,
)


def get_data():
    try:
        with open(DATA_PATH / "group_mute_data.json", "r", encoding="utf8") as f:
            data = json.load(f)
    except (ValueError, FileNotFoundError):
        data = {}
    return data


def save_data():
    global mute_data
    with open(DATA_PATH / "group_mute_data.json", "w", encoding="utf8") as f:
        json.dump(mute_data, f, indent=4)


async def download_img_and_hash(url, group_id):
    if await AsyncHttpx.download_file(
        url, TEMP_PATH / f"mute_{group_id}_img.jpg"
    ):
        return str(get_img_hash(TEMP_PATH / f"mute_{group_id}_img.jpg"))
    return ""


mute_dict = {}
mute_data = get_data()


@mute.handle()
async def _(bot: Bot, event: GroupMessageEvent, cmd: Tuple[str, ...] = Command(), arg: Message = CommandArg()):
    group_id = str(event.group_id)
    msg = arg.extract_plain_text().strip()
    img_list = get_message_img(event.json())
    img_hash = ""
    for img in img_list:
        img_hash += await download_img_and_hash(img, event.group_id)
    msg += img_hash
    if not mute_data.get(group_id):
        mute_data[group_id] = {
            "count": Config.get_config("mute", "MUTE_DEFAULT_COUNT"),
            "time": Config.get_config("mute", "MUTE_DEFAULT_TIME"),
            "duration": Config.get_config("mute", "MUTE_DEFAULT_DURATION"),
        }
    if not mute_dict.get(event.user_id):
        mute_dict[event.user_id] = {"time": time.time(), "count": 1, "msg": msg}
    else:
        if cmd or not msg:
            return
        if msg and msg.find(mute_dict[event.user_id]["msg"]) != -1:
            mute_dict[event.user_id]["count"] += 1
        else:
            mute_dict[event.user_id]["time"] = time.time()
            mute_dict[event.user_id]["count"] = 1
        mute_dict[event.user_id]["msg"] = msg
        if time.time() - mute_dict[event.user_id]["time"] > mute_data[group_id]["time"]:
            mute_dict[event.user_id]["time"] = time.time()
            mute_dict[event.user_id]["count"] = 1
        if (
            mute_dict[event.user_id]["count"] > mute_data[group_id]["count"]
            and time.time() - mute_dict[event.user_id]["time"]
            < mute_data[group_id]["time"]
        ):
            try:
                if mute_data[group_id]["duration"] != 0:
                    await bot.set_group_ban(
                        group_id=event.group_id,
                        user_id=event.user_id,
                        duration=mute_data[group_id]["duration"],
                    )
                    await mute.send(f"检测到恶意刷屏，{NICKNAME}要把你关进小黑屋！", at_sender=True)
                    mute_dict[event.user_id]["count"] = 0
                    logger.info(
                        f"USER {event.user_id} GROUP {event.group_id} "
                        f'检测刷屏 被禁言 {mute_data[group_id]["duration"] / 60} 分钟'
                    )
            except ActionFailed:
                pass


@mute_setting.handle()
async def _(event: GroupMessageEvent, cmd: Tuple[str, ...] = Command(), arg: Message = CommandArg()):
    group_id = str(event.group_id)
    if not mute_data.get(group_id):
        mute_data[group_id] = {"count": 10, "time": 7, "duration": 0}
    msg = arg.extract_plain_text().strip()
    if cmd[0] == "刷屏检测设置":
        await mute_setting.finish(
            f'最大次数：{mute_data[group_id]["count"]} 次\n'
            f'规定时间：{mute_data[group_id]["time"]} 秒\n'
            f'禁言时长：{mute_data[group_id]["duration"] / 60} 分钟\n'
            f"【在规定时间内发送相同消息超过最大次数则禁言\n当禁言时长为0时关闭此功能】"
        )
    if not is_number(msg):
        await mute.finish("设置的参数必须是数字啊！", at_sender=True)
    if cmd[0] == "设置检测时间":
        mute_data[group_id]["time"] = int(msg)
        msg += "秒"
    if cmd[0] == "设置检测次数":
        mute_data[group_id]["count"] = int(msg)
        msg += " 次"
    if cmd[0] == "设置禁言时长":
        mute_data[group_id]["duration"] = int(msg) * 60
        msg += " 分钟"
    await mute_setting.send(f'刷屏检测：{cmd[0]}为 {msg}')
    logger.info(
        f'USER {event.user_id} GROUP {group_id} {cmd[0]}：{msg}'
    )
    save_data()
