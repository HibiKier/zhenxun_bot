from datetime import datetime
from typing import Any, List, Tuple

from nonebot import on_command, on_message, on_regex
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GroupMessageEvent,
    Message,
    MessageEvent,
)
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.params import CommandArg, RegexGroup
from nonebot.permission import SUPERUSER

from configs.config import NICKNAME, Config
from models.ban_user import BanUser
from services.log import logger
from utils.image_utils import BuildImage
from utils.manager import group_manager
from utils.message_builder import image
from utils.utils import get_message_text, is_number

from .data_source import set_user_punish, show_black_text_image
from .model import BlackWord
from .utils import black_word_manager

__zx_plugin_name__ = "敏感词检测"
__plugin_usage__ = """
usage：
    注意你的发言！
    指令：
        惩罚机制
""".strip()
__plugin_superuser_usage__ = """
usage：
    查看和设置惩罚
    Regex：^记录名单(u:\d*)?(g:\d*)?(d[=><]\d*-\d{1,2}-\d{1,2})?$
    设置惩罚id需要通过 '记录名单u:xxxxxxxx' 获取
    指令：
        记录名单
        设置惩罚 [user_id] [下标] [惩罚等级]
        示例：记录名单
        示例：记录名单u:12345678
        示例：设置惩罚 12345678 1 4
""".strip()
__plugin_des__ = "请注意你的发言！！"
__plugin_type__ = ("其他",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_cmd__ = ["惩罚机制", "记录名单 [_superuser]", "设置惩罚 [_superuser]"]
__plugin_settings__ = {
    "cmd": ["敏感词检测"],
}


Config.add_plugin_config(
    "black_word",
    "CYCLE_DAYS",
    30,
    name="敏感词检测与惩罚",
    help_="黑名单词汇记录周期",
    default_value=30,
    type=int,
)

Config.add_plugin_config(
    "black_word",
    "TOLERATE_COUNT",
    [5, 1, 1, 1, 1],
    help_="各个级别惩罚的容忍次数，依次为：1, 2, 3, 4, 5",
    default_value=[5, 1, 1, 1, 1],
    type=List[int],
)

Config.add_plugin_config(
    "black_word", "AUTO_PUNISH", True, help_="是否启动自动惩罚机制", default_value=True, type=bool
)

# Config.add_plugin_config(
#     "black_word", "IGNORE_GROUP", [], help_="退出群聊惩罚中忽略的群聊，即不会退出的群聊", default_value=[]
# )

Config.add_plugin_config(
    "black_word",
    "BAN_4_DURATION",
    360,
    help_="Union[int, List[int, int]]Ban时长（分钟），四级惩罚，可以为指定数字或指定列表区间(随机)，例如 [30, 360]",
    default_value=360,
    type=int,
)

Config.add_plugin_config(
    "black_word",
    "BAN_3_DURATION",
    7,
    help_="Union[int, List[int, int]]Ban时长（天），三级惩罚，可以为指定数字或指定列表区间(随机)，例如 [7, 30]",
    default_value=7,
    type=int,
)

Config.add_plugin_config(
    "black_word",
    "WARNING_RESULT",
    f"请注意对{NICKNAME}的发言内容",
    help_="口头警告内容",
    default_value=f"请注意对{NICKNAME}的发言内容",
)

Config.add_plugin_config(
    "black_word",
    "AUTO_ADD_PUNISH_LEVEL",
    True,
    help_="自动提级机制，当周期内处罚次数大于某一特定值就提升惩罚等级",
    default_value=True,
    type=bool,
)

Config.add_plugin_config(
    "black_word",
    "ADD_PUNISH_LEVEL_TO_COUNT",
    3,
    help_="在CYCLE_DAYS周期内触发指定惩罚次数后提升惩罚等级",
    default_value=3,
    type=int,
)

Config.add_plugin_config(
    "black_word",
    "ALAPI_CHECK_FLAG",
    False,
    help_="当未检测到已收录的敏感词时，开启ALAPI文本检测并将疑似文本发送给超级用户",
    default_value=False,
    type=bool,
)

Config.add_plugin_config(
    "black_word",
    "CONTAIN_BLACK_STOP_PROPAGATION",
    True,
    help_="当文本包含任意敏感词时，停止向下级插件传递，即不触发ai",
    default_value=True,
    type=bool,
)

message_matcher = on_message(priority=1, block=False)

set_punish = on_command("设置惩罚", priority=1, permission=SUPERUSER, block=True)

show_black = on_regex(
    r"^记录名单(u:\d*)?(g:\d*)?(d[=><]\d*-\d{1,2}-\d{1,2})?$",
    priority=1,
    permission=SUPERUSER,
    block=True,
)

show_punish = on_command("惩罚机制", aliases={"敏感词检测"}, priority=1, block=True)


# 黑名单词汇检测
@run_preprocessor
async def _(
    bot: Bot,
    matcher: Matcher,
    event: Event,
):
    msg = get_message_text(event.json())
    if (
        isinstance(event, MessageEvent)
        and event.is_tome()
        and not msg.startswith("原神绑定")
    ):
        if str(event.user_id) in bot.config.superusers:
            return logger.debug(f"超级用户跳过黑名单词汇检查 Message: {msg}", target=event.user_id)
        if (
            event.is_tome()
            and matcher.plugin_name == "black_word"
            and not await BanUser.is_ban(event.user_id)
        ):
            # 屏蔽群权限-1的群
            if (
                isinstance(event, GroupMessageEvent)
                and group_manager.get_group_level(event.group_id) < 0
            ):
                return
            user_id = str(event.user_id)
            group_id = str(event.group_id) if isinstance(event, GroupMessageEvent) else None
            msg = get_message_text(event.json())
            if await black_word_manager.check(
                user_id, group_id, msg
            ) and Config.get_config("black_word", "CONTAIN_BLACK_STOP_PROPAGATION"):
                matcher.stop_propagation()


@show_black.handle()
async def _(bot: Bot, reg_group: Tuple[Any, ...] = RegexGroup()):
    user_id, group_id, date = reg_group
    date_type = "="
    if date:
        date_type = date[1]
        date = date[2:]
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            await show_black.finish("日期格式错误，需要：年-月-日")
    pic = await show_black_text_image(
        bot,
        user_id.split(":")[1] if user_id else None,
        group_id.split(":")[1] if group_id else None,
        date,
        date_type,
    )
    await show_black.send(image(b64=pic.pic2bs4()))


@show_punish.handle()
async def _():
    text = f"""
    ** 惩罚机制 **

    惩罚前包含容忍机制，在指定周期内会容忍偶尔少次数的敏感词只会进行警告提醒

    多次触发同级惩罚会使惩罚等级提高，即惩罚自动提级机制

    目前公开的惩罚等级：

        1级：永久ban

        2级：删除好友

        3级：ban指定/随机天数

        4级：ban指定/随机时长

        5级：警告

    备注：

        该功能为测试阶段，如果你有被误封情况，请联系管理员，会从数据库中提取出你的数据进行审核后判断

        目前该功能暂不完善，部分情况会由管理员鉴定，请注意对真寻的发言
    
    关于敏感词：
        
        记住不要骂{NICKNAME}就对了！
    """.strip()
    max_width = 0
    for m in text.split("\n"):
        max_width = len(m) * 20 if len(m) * 20 > max_width else max_width
    max_height = len(text.split("\n")) * 24
    A = BuildImage(
        max_width, max_height, font="CJGaoDeGuo.otf", font_size=24, color="#E3DBD1"
    )
    A.text((10, 10), text)
    await show_punish.send(image(b64=A.pic2bs4()))


@set_punish.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    if (
        len(msg) < 3
        or not is_number(msg[0])
        or not is_number(msg[1])
        or not is_number(msg[2])
    ):
        await set_punish.finish("参数错误，请查看帮助...", at_sender=True)
    uid = msg[0]
    id_ = int(msg[1])
    punish_level = int(msg[2])
    rst = await set_user_punish(uid, id_, punish_level)
    await set_punish.send(rst)
    logger.info(
        f"设置惩罚 uid：{uid} id_：{id_} punish_level:{punish_level} --> {rst}",
        "设置惩罚",
        event.user_id,
    )
