from nonebot.adapters import Bot
from nonebot.adapters.kaiheila.exception import ApiNotAvailable
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, Arparma, At, Match, on_alconna
from nonebot_plugin_saa import Mention, MessageFactory, Text
from nonebot_plugin_session import EventSession, SessionLevel

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.friend_user import FriendUser
from zhenxun.models.group_info import GroupInfo
from zhenxun.models.level_user import LevelUser
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

__plugin_meta__ = PluginMetadata(
    name="更新群组/好友信息",
    description="更新群组/好友信息",
    usage="""
    更新群组信息
    更新好友信息
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)


_group_matcher = on_alconna(
    Alconna(
        "更新群组信息",
    ),
    permission=SUPERUSER,
    rule=to_me(),
    priority=1,
    block=True,
)

_friend_matcher = on_alconna(
    Alconna(
        "更新好友信息",
    ),
    permission=SUPERUSER,
    rule=to_me(),
    priority=1,
    block=True,
)

# TODO: 其他adapter的更新操作

@_group_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
):
    try:
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        num = 0
        for g in gl:
            try:
                group_info = await bot.get_group_info(group_id=g)
                await GroupInfo.update_or_create(
                    group_id=str(group_info["group_id"]),
                    defaults={
                        "group_name": group_info["group_name"],
                        "max_member_count": group_info["max_member_count"],
                        "member_count": group_info["member_count"],
                    },
                )
                num += 1
                logger.debug(
                    "群聊信息更新成功", "更新群信息", session=session, target=group_info["group_id"]
                )
            except Exception as e:
                logger.error(
                    f"更新群聊信息失败",
                    arparma.header_result,
                    session=session,
                    target=g,
                )
        await Text(f"成功更新了 {len(gl)} 个群的信息").send()
        logger.info(
            f"更新群聊信息完成，共更新了 {len(gl)} 个群的信息", arparma.header_result, session=session
        )
    except (ApiNotAvailable, AttributeError) as e:
        await Text("Api未实现...").send()
    except Exception as e:
        logger.error("更新好友信息发生错误", arparma.header_result, session=session, e=e)
        await Text("其他未知错误...").send()


@_friend_matcher.assign("delete")
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
):
    num = 0
    error_list = []
    fl = await bot.get_friend_list()
    for f in fl:
        try:
            await FriendUser.update_or_create(
                user_id=str(f["user_id"]), defaults={"nickname": f["nickname"]}
            )
            logger.debug(f"更新好友信息成功", "更新好友信息", session=session, target=f["user_id"])
            num += 1
        except Exception as e:
            logger.error(f"更新好友信息失败", "更新好友信息", session=session, target=f["user_id"], e=e)
    await Text(f"成功更新了 {num} 个好友的信息!").send()
    if error_list:
        await Text(f"以下好友更新失败:\n" + "\n".join(error_list)).send()
    logger.info(f"更新好友信息完成，共更新了 {num} 个群的信息", arparma.header_result, session=session)
