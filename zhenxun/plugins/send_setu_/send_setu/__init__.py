import random
from typing import Tuple

from nonebot.adapters import Bot
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor
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

from zhenxun.configs.config import NICKNAME
from zhenxun.configs.utils import PluginCdBlock, PluginExtraData, RegisterConfig
from zhenxun.models.sign_user import SignUser
from zhenxun.models.user_console import UserConsole
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils
from zhenxun.utils.withdraw_manage import WithdrawManager

from ._data_source import SetuManage, base_config

__plugin_meta__ = PluginMetadata(
    name="色图",
    description="不要小看涩图啊混蛋！",
    usage="""
    搜索 lolicon 图库，每日色图time...
    多个tag使用#连接
    指令：
        色图: 随机色图
        色图 -r: 随机在线r18涩图
        色图 -id [id]: 本地指定id色图
        色图 *[tags]: 在线搜索指定tag色图
        色图 *[tags] -r: 同上, r18色图
        [1-9]张涩图: 本地随机色图连发
        [1-9]张[tags]的涩图: 在线搜索指定tag色图连发
    示例：色图 萝莉|少女#白丝|黑丝
    示例：色图 萝莉#猫娘
    注：
        tag至多取前20项，| 为或，萝莉|少女=萝莉或者少女
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="来点好康的",
        limits=[PluginCdBlock(result="您冲的太快了，请稍后再冲.")],
        configs=[
            RegisterConfig(
                key="WITHDRAW_SETU_MESSAGE",
                value=(0, 1),
                help="自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
                default_value=(0, 1),
                type=Tuple[int, int],
            ),
            RegisterConfig(
                key="ONLY_USE_LOCAL_SETU",
                value=False,
                help="仅仅使用本地色图，不在线搜索",
                default_value=False,
                type=bool,
            ),
            RegisterConfig(
                key="INITIAL_SETU_PROBABILITY",
                value=0.7,
                help="初始色图概率，总概率 = 初始色图概率 + 好感度",
                default_value=0.7,
                type=float,
            ),
            RegisterConfig(
                key="DOWNLOAD_SETU",
                value=True,
                help="是否存储下载的色图，使用本地色图可以加快图片发送速度",
                default_value=True,
                type=float,
            ),
            RegisterConfig(
                key="TIMEOUT",
                value=10,
                help="色图下载超时限制(秒)",
                default_value=10,
                type=int,
            ),
            RegisterConfig(
                key="SHOW_INFO",
                value=True,
                help="是否显示色图的基本信息，如PID等",
                default_value=True,
                type=bool,
            ),
            RegisterConfig(
                key="ALLOW_GROUP_R18",
                value=False,
                help="在群聊中启用R18权限",
                default_value=False,
                type=bool,
            ),
            RegisterConfig(
                key="MAX_ONCE_NUM2FORWARD",
                value=None,
                help="单次发送的图片数量达到指定值时转发为合并消息",
                default_value=None,
                type=int,
            ),
            RegisterConfig(
                key="MAX_ONCE_NUM",
                value=10,
                help="单次发送图片数量限制",
                default_value=10,
                type=int,
            ),
            RegisterConfig(
                module="pixiv",
                key="PIXIV_NGINX_URL",
                value="i.pixiv.re",
                help="Pixiv反向代理",
                default_value="i.pixiv.re",
            ),
        ],
    ).dict(),
)


@run_postprocessor
async def _(
    matcher: Matcher,
    exception: Exception | None,
    session: EventSession,
):
    if matcher.plugin_name == "send_setu":
        # 添加数据至数据库
        try:
            await SetuManage.save_to_database()
            logger.info("色图数据自动存储数据库成功...")
        except Exception:
            pass


_matcher = on_alconna(
    Alconna(
        "色图",
        Args["tags?", str],
        Option("-n", Args["num", int, 1], help_text="数量"),
        Option("-id", Args["local_id", int], help_text="本地id"),
        Option("-r", action=store_true, help_text="r18"),
    ),
    aliases={"涩图", "不够色", "来一发", "再来点"},
    priority=5,
    block=True,
)

_matcher.shortcut(
    r".*?(?P<num>\d*)[份|发|张|个|次|点](?P<tags>.*)[瑟|色|涩]图.*?",
    command="色图",
    arguments=["{tags}", "-n", "{num}"],
    prefix=True,
)


@_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    num: Match[int],
    tags: Match[str],
    local_id: Match[int],
):
    _tags = tags.result.split("#") if tags.available else None
    if _tags and NICKNAME in _tags:
        await MessageUtils.build_message(
            "咳咳咳，虽然我很可爱，但是我木有自己的色图~~~有的话记得发我一份呀"
        ).finish()
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    gid = session.id3 or session.id2
    user_console = await UserConsole.get_user(session.id1, session.platform)
    user, _ = await SignUser.get_or_create(
        user_id=session.id1,
        defaults={"user_console": user_console, "platform": session.platform},
    )
    if session.id1 not in bot.config.superusers:
        """超级用户跳过罗翔"""
        if result := SetuManage.get_luo(float(user.impression)):
            await result.finish()
    is_r18 = arparma.find("r")
    _num = num.result if num.available else 1
    if is_r18 and gid:
        """群聊中禁止查看r18"""
        if not base_config.get("ALLOW_GROUP_R18"):
            await MessageUtils.build_message(
                random.choice(
                    [
                        "这种不好意思的东西怎么可能给这么多人看啦",
                        "羞羞脸！给我滚出克私聊！",
                        "变态变态变态变态大变态！",
                    ]
                )
            ).finish()
    if local_id.available:
        """指定id"""
        result = await SetuManage.get_setu(local_id=local_id.result)
        if isinstance(result, str):
            await MessageUtils.build_message(result).finish(reply_to=True)
        await result[0].finish()
    result_list = await SetuManage.get_setu(tags=_tags, num=_num, is_r18=is_r18)
    if isinstance(result_list, str):
        await MessageUtils.build_message(result_list).finish(reply_to=True)
    max_once_num2forward = base_config.get("MAX_ONCE_NUM2FORWARD")
    platform = PlatformUtils.get_platform(bot)
    if (
        "qq" == platform
        and gid
        and max_once_num2forward
        and len(result_list) >= max_once_num2forward
    ):
        logger.debug("使用合并转发转发色图数据", arparma.header_result, session=session)
        forward = MessageUtils.template2forward(result_list, bot.self_id)  # type: ignore
        await bot.send_group_forward_msg(
            group_id=int(gid),
            messages=forward,  # type: ignore
        )
    else:
        for result in result_list:
            logger.info(f"发送色图 {result}", arparma.header_result, session=session)
            receipt = await result.send()
            if receipt:
                message_id = receipt.msg_ids[0]["message_id"]
                await WithdrawManager.withdraw_message(
                    bot,
                    message_id,
                    base_config.get("WITHDRAW_SETU_MESSAGE"),
                    session,
                )
    logger.info(
        f"调用发送 {num}张 色图 tags: {_tags}", arparma.header_result, session=session
    )
