from datetime import datetime
from typing import List

from nonebot.adapters import Bot
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, Option, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import NICKNAME
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.message import MessageUtils

from .data_source import set_user_punish, show_black_text_image

__plugin_meta__ = PluginMetadata(
    name="敏感词检测",
    description="请注意你的发言！",
    usage="""
    惩罚机制: 检测内容提示
    设置惩罚 [uid] [id] [level]: 设置惩罚内容, 此id需要通过`记录名单 -u:uid`来获取
    记录名单: 查看检测记录名单
    记录名单:
        -u [uid] 指定用户记录名单
        -g [gid] 指定群组记录名单
        -d [date] 指定日期
        -dt ['=', '>', '<'] 大于小于等于指定日期

    示例:
        设置惩罚 123123123 0 1
        记录名单 -u 123123123
        记录名单 -g 333333
        记录名单 -d 2022-11-11
        记录名单 -d 2022-11-11 -dt >
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
        menu_type="其他",
        configs=[
            RegisterConfig(
                key="CYCLE_DAYS",
                value=30,
                help="黑名单词汇记录周期",
                default_value=30,
                type=int,
            ),
            RegisterConfig(
                key="TOLERATE_COUNT",
                value=[5, 1, 1, 1, 1],
                help="各个级别惩罚的容忍次数, 依次为: 1, 2, 3, 4, 5",
                default_value=[5, 1, 1, 1, 1],
                type=List[int],
            ),
            RegisterConfig(
                key="AUTO_PUNISH",
                value=True,
                help="是否启动自动惩罚机制",
                default_value=True,
                type=bool,
            ),
            RegisterConfig(
                key="BAN_4_DURATION",
                value=360,
                help="Ban时长（分钟），四级惩罚，可以为指定数字或指定列表区间(随机)，例如 [30, 360]",
                default_value=360,
                type=int,
            ),
            RegisterConfig(
                key="BAN_3_DURATION",
                value=7,
                help="Ban时长（天），三级惩罚，可以为指定数字或指定列表区间(随机)，例如 [7, 30]",
                default_value=7,
                type=int,
            ),
            RegisterConfig(
                key="WARNING_RESULT",
                value=f"请注意对{NICKNAME}的发言内容",
                help="口头警告内容",
                default_value=None,
            ),
            RegisterConfig(
                key="AUTO_ADD_PUNISH_LEVEL",
                value=360,
                help="自动提级机制，当周期内处罚次数大于某一特定值就提升惩罚等级",
                default_value=360,
                type=int,
            ),
            RegisterConfig(
                key="ADD_PUNISH_LEVEL_TO_COUNT",
                value=3,
                help="在CYCLE_DAYS周期内触发指定惩罚次数后提升惩罚等级",
                default_value=3,
                type=int,
            ),
            RegisterConfig(
                key="ALAPI_CHECK_FLAG",
                value=False,
                help="当未检测到已收录的敏感词时，开启ALAPI文本检测并将疑似文本发送给超级用户",
                default_value=False,
                type=bool,
            ),
            RegisterConfig(
                key="CONTAIN_BLACK_STOP_PROPAGATION",
                value=True,
                help="当文本包含任意敏感词时，停止向下级插件传递，即不触发ai",
                default_value=True,
                type=bool,
            ),
        ],
    ).dict(),
)


_punish_matcher = on_alconna(
    Alconna("设置惩罚", Args["uid", str]["id", int]["punish_level", int]),
    priority=1,
    permission=SUPERUSER,
    block=True,
)


_show_matcher = on_alconna(
    Alconna(
        "记录名单",
        Option("-u|--uid", Args["uid", str]),
        Option("-g|--group", Args["gid", str]),
        Option("-d|--date", Args["date", str]),
        Option("-dt|--type", Args["date_type", ["=", ">", "<"]], default="="),
    ),
    priority=1,
    permission=SUPERUSER,
    block=True,
)

_show_punish_matcher = on_alconna(
    Alconna("惩罚机制"), aliases={"敏感词检测"}, priority=1, block=True
)


@_show_matcher.handle()
async def _(
    bot: Bot, uid: Match[str], gid: Match[str], date: Match[str], date_type: Match[str]
):
    user_id = None
    group_id = None
    date_ = None
    date_str = None
    date_type_ = "="
    if uid.available:
        user_id = uid.result
    if gid.available:
        group_id = gid.result
    if date.available:
        date_str = date.result
    if date_type.available:
        date_type_ = date_type.result
    if date_str:
        try:
            date_ = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            await MessageUtils.build_message("日期格式错误，需要：年-月-日").finish()
    result = await show_black_text_image(
        user_id,
        group_id,
        date_,
        date_type_,
    )
    await MessageUtils.build_message(result).send()


@_show_punish_matcher.handle()
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
    await A.text((10, 10), text)
    await MessageUtils.build_message(A).send()


@_punish_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    uid: str,
    id: int,
    punish_level: int,
):
    result = await set_user_punish(
        bot, uid, session.id2 or session.id3, id, punish_level
    )
    await MessageUtils.build_message(result).send(reply_to=True)
    logger.info(
        f"设置惩罚 uid:{uid} id_:{id} punish_level:{punish_level} --> {result}",
        arparma.header_result,
        session=session,
    )
