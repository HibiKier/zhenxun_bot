import random
from pathlib import Path

import ujson as json
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import DATA_PATH
from zhenxun.models.ban_console import BanConsole
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.platform import PlatformUtils
from zhenxun.utils.utils import cn2py

from .model import BlackWord


class BlackWordManager:
    """
    敏感词管理（ 拒绝恶意
    """

    def __init__(self, word_file: Path, py_file: Path):
        self._word_list = {
            "1": [],
            "2": [],
            "3": [],
            "4": ["sb", "nmsl", "mdzz", "2b", "jb", "操", "废物", "憨憨", "cnm", "rnm"],
            "5": [],
        }
        self._py_list = {
            "1": [],
            "2": [],
            "3": [],
            "4": [
                "shabi",
                "wocaonima",
                "sima",
                "sabi",
                "zhizhang",
                "naocan",
                "caonima",
                "rinima",
                "simadongxi",
                "simawanyi",
                "hanbi",
                "hanpi",
                "laji",
                "fw",
            ],
            "5": [],
        }
        word_file.parent.mkdir(parents=True, exist_ok=True)
        if word_file.exists():
            # 清空默认配置
            with open(word_file, "r", encoding="utf8") as f:
                self._word_list = json.load(f)
        else:
            with open(word_file, "w", encoding="utf8") as f:
                json.dump(
                    self._word_list,
                    f,
                    ensure_ascii=False,
                    indent=4,
                )
        if py_file.exists():
            # 清空默认配置
            with open(py_file, "r", encoding="utf8") as f:
                self._py_list = json.load(f)
        else:
            with open(py_file, "w", encoding="utf8") as f:
                json.dump(
                    self._py_list,
                    f,
                    ensure_ascii=False,
                    indent=4,
                )

    async def check(
        self, bot: Bot, session: EventSession, message: str
    ) -> str | bool | None:
        """检查是否包含黑名单词汇

        参数:
            bot: Bot
            session: EventSession
            message: 消息
        """
        logger.debug(
            f"检查文本是否含有黑名单词汇: {message}", "敏感词检测", session=session
        )
        if session.id1:
            if data := self._check(message):
                if data[0]:
                    await _add_user_black_word(
                        bot,
                        session.id1,
                        session.id2 or session.id3,
                        data[0],
                        message,
                        int(data[1]),
                    )
                    return True
            if Config.get_config(
                "black_word", "ALAPI_CHECK_FLAG"
            ) and not await check_text(message):
                await send_msg(
                    bot,
                    "",
                    None,
                    f"用户 {session.id1} 群组 {session.id3 or session.id2} ALAPI 疑似检测：{message}",
                )
        return False

    def _check(self, message: str) -> tuple[str | None, int]:
        """检测文本是否违规

        参数:
            message: 检测消息
        """
        # 移除空格
        message = message.replace(" ", "")
        py_msg = cn2py(message).lower()
        # 完全匹配
        for x in [self._word_list, self._py_list]:
            for level in x:
                if message in x[level] or py_msg in x[level]:
                    return message if message in x[level] else py_msg, int(level)
        # 模糊匹配
        for x in [self._word_list, self._py_list]:
            for level in x:
                for m in x[level]:
                    if m in message or m in py_msg:
                        return m, -1
        return None, 0


async def _add_user_black_word(
    bot: Bot,
    user_id: str,
    group_id: str | None,
    black_word: str,
    message: str,
    punish_level: int,
):
    """添加敏感词数据

    参数:
        bot: Bot
        user_id: 用户id
        group_id: 群组id或频道id
        black_word: 触发的黑名单词汇
        message: 原始文本
        punish_level: 惩罚等级
    """
    cycle_days = Config.get_config("black_word", "CYCLE_DAYS") or 7
    user_count = await BlackWord.get_user_count(user_id, cycle_days, punish_level)
    add_punish_level_to_count = Config.get_config(
        "black_word", "ADD_PUNISH_LEVEL_TO_COUNT"
    )
    # 周期内超过次数直接提升惩罚
    if (
        Config.get_config("black_word", "AUTO_ADD_PUNISH_LEVEL")
        and add_punish_level_to_count
    ):
        punish_level -= 1
    await BlackWord.create(
        user_id=user_id,
        group_id=group_id,
        plant_text=message,
        black_word=black_word,
        punish_level=punish_level,
        platform=PlatformUtils.get_platform(bot),
    )
    logger.info(
        f"已将 USER {user_id} GROUP {group_id} 添加至黑名单词汇记录 Black_word：{black_word} Plant_text：{message}"
    )
    # 自动惩罚
    if Config.get_config("black_word", "AUTO_PUNISH") and punish_level != -1:
        await _punish_handle(bot, user_id, group_id, punish_level, black_word)


async def _punish_handle(
    bot: Bot,
    user_id: str,
    group_id: str | None,
    punish_level: int,
    black_word: str,
):
    """惩罚措施，级别越低惩罚越严

    参数:
        bot: Bot
        user_id: 用户id
        group_id: 群组id或频道id
        black_word: 触发的黑名单词汇
        channel_id: 频道id
    """
    logger.info(f"BlackWord USER {user_id} 触发 {punish_level} 级惩罚...")
    # 周期天数
    cycle_days = Config.get_config("black_word", "CYCLE_DAYS") or 7
    # 用户周期内触发punish_level级惩罚的次数
    user_count = await BlackWord.get_user_count(user_id, cycle_days, punish_level)
    # 获取最近一次的惩罚等级，将在此基础上增加
    punish_level = (
        await BlackWord.get_user_punish_level(user_id, cycle_days) or punish_level
    )
    # 容忍次数：List[int]
    tolerate_count = Config.get_config("black_word", "TOLERATE_COUNT")
    if not tolerate_count or len(tolerate_count) < 5:
        tolerate_count = [5, 2, 2, 2, 2]
    if punish_level == 1 and user_count > tolerate_count[punish_level - 1]:
        # 永久ban
        await _get_punish(bot, 1, user_id, group_id)
        await BlackWord.set_user_punish(user_id, "永久ban 删除好友", black_word)
    elif punish_level == 2 and user_count > tolerate_count[punish_level - 1]:
        # 删除好友
        await _get_punish(bot, 2, user_id, group_id)
        await BlackWord.set_user_punish(user_id, "删除好友", black_word)
    elif punish_level == 3 and user_count > tolerate_count[punish_level - 1]:
        # 永久ban
        ban_day = await _get_punish(bot, 3, user_id, group_id)
        await BlackWord.set_user_punish(user_id, f"ban {ban_day} 天", black_word)
    elif punish_level == 4 and user_count > tolerate_count[punish_level - 1]:
        # ban指定时长
        ban_time = await _get_punish(bot, 4, user_id, group_id)
        await BlackWord.set_user_punish(user_id, f"ban {ban_time} 分钟", black_word)
    elif punish_level == 5 and user_count > tolerate_count[punish_level - 1]:
        # 口头警告
        warning_result = await _get_punish(bot, 5, user_id, group_id)
        await BlackWord.set_user_punish(
            user_id, f"口头警告：{warning_result}", black_word
        )
    else:
        await BlackWord.set_user_punish(user_id, f"提示！", black_word)
        await send_msg(
            bot,
            user_id,
            group_id,
            f"BlackWordChecker：该条发言已被记录，目前你在{cycle_days}天内的发表{punish_level}级"
            f"言论记录次数为：{user_count}次，请注意你的发言\n"
            f"* 如果你不清楚惩罚机制，请发送“惩罚机制” *",
        )


async def _get_punish(
    bot: Bot,
    id_: int,
    user_id: str,
    group_id: str | None = None,
) -> int | str | None:
    """通过id_获取惩罚

    参数:
        bot: Bot
        id_: id
        user_id: 用户id
        group_id: 群组id或频道id
    """
    # 忽略的群聊
    # _ignore_group = Config.get_config("black_word", "IGNORE_GROUP")
    # 处罚 id 4 ban 时间：int，List[int]
    ban_3_duration = Config.get_config("black_word", "BAN_3_DURATION") or 7
    # 处罚 id 4 ban 时间：int，List[int]
    ban_4_duration = Config.get_config("black_word", "BAN_4_DURATION") or 360
    # 口头警告内容
    warning_result = Config.get_config("black_word", "WARNING_RESULT")
    if user := await GroupInfoUser.get_or_none(user_id=user_id, group_id=group_id):
        uname = user.user_name
    else:
        uname = user_id
    # 永久ban
    if id_ == 1:
        if str(user_id) not in bot.config.superusers:
            await BanConsole.ban(user_id, group_id, 10, -1, None)
            await send_msg(
                bot,
                user_id,
                group_id,
                f"BlackWordChecker 永久ban USER {uname}({user_id})",
            )
            logger.info(f"BlackWord 永久封禁 USER {user_id}...")
    # 删除好友（有的话
    elif id_ == 2:
        if str(user_id) not in bot.config.superusers:
            try:
                await bot.delete_friend(user_id=user_id)
                await send_msg(
                    bot,
                    user_id,
                    group_id,
                    f"BlackWordChecker 删除好友 USER {uname}({user_id})",
                )
                logger.info(f"BlackWord 删除好友 {user_id}...")
            except ActionFailed:
                pass
    # 封禁用户指定时间，默认7天
    elif id_ == 3:
        if isinstance(ban_3_duration, list):
            ban_3_duration = random.randint(ban_3_duration[0], ban_3_duration[1])
        await BanConsole.ban(user_id, group_id, 9, ban_4_duration * 60 * 24)
        await send_msg(
            bot,
            user_id,
            group_id,
            f"BlackWordChecker 对用户 USER {uname}({user_id}) 进行封禁 {ban_3_duration} 天处罚。",
        )
        logger.info(f"BlackWord 封禁 USER {uname}({user_id}) {ban_3_duration} 天...")
        return ban_3_duration
    # 封禁用户指定时间，默认360分钟
    elif id_ == 4:
        if isinstance(ban_4_duration, list):
            ban_4_duration = random.randint(ban_4_duration[0], ban_4_duration[1])
        await BanConsole.ban(user_id, group_id, 9, ban_4_duration * 60)
        await send_msg(
            bot,
            user_id,
            group_id,
            f"BlackWordChecker 对用户 USER {uname}({user_id}) 进行封禁 {ban_4_duration} 分钟处罚。",
        )
        logger.info(f"BlackWord 封禁 USER {uname}({user_id}) {ban_4_duration} 分钟...")
        return ban_4_duration
    # 口头警告
    elif id_ == 5:
        await PlatformUtils.send_message(bot, user_id, group_id, warning_result)
        logger.info(f"BlackWord 口头警告 USER {user_id}")
        return warning_result
    return None


async def send_msg(bot: Bot, user_id: str, group_id: str | None, message: str):
    """发送消息

    参数:
        bot: Bot
        user_id: user_id
        group_id: group_id
        message: message
    """
    if not user_id:
        platform = PlatformUtils.get_platform(bot)
        user_id = bot.config.platform_superusers[platform][0]
    await PlatformUtils.send_message(bot, user_id, group_id, message)


async def check_text(text: str) -> bool:
    """ALAPI文本检测，检测输入违规

    参数:
        text: 回复
    """
    if not Config.get_config("alapi", "ALAPI_TOKEN"):
        return True
    params = {"token": Config.get_config("alapi", "ALAPI_TOKEN"), "text": text}
    try:
        data = (
            await AsyncHttpx.get(
                "https://v2.alapi.cn/api/censor/text", timeout=4, params=params
            )
        ).json()
        if data["code"] == 200:
            return data["data"]["conclusion_type"] == 2
    except Exception as e:
        logger.error(f"检测违规文本错误...", e=e)
    return True


black_word_manager = BlackWordManager(
    DATA_PATH / "black_word" / "black_word.json",
    DATA_PATH / "black_word" / "black_py.json",
)
