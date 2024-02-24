from nonebot.adapters import Bot
from nonebot.adapters.kaiheila.exception import ApiNotAvailable
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import Alconna, on_alconna
from nonebot_plugin_alconna.matcher import AlconnaMatcher
from nonebot_plugin_saa import Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import DATA_PATH
from zhenxun.configs.utils import ConfigModel, PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.rules import admin_check, ensure_group

__plugin_meta__ = PluginMetadata(
    name="好友群组列表",
    description="查看好友群组列表以",
    usage="""
        查看所有好友
        查看所有群组
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)

_friend_matcher = on_alconna(
    Alconna("好友列表"),
    rule=to_me(),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

_group_matcher = on_alconna(
    Alconna("群组列表"),
    rule=to_me(),
    permission=SUPERUSER,
    priority=1,
    block=True,
)

# _friend_handle_matcher = on_alconna(
#     Alconna(
#         "好友操作",
#         Subcommand("delete", Args["uid", str], help_text="删除好友"),
#         Subcommand("send", Args["uid", str]["message", str], help_text="发送消息"),
#     )
# )

# _group_handle_matcher = on_alconna(
#     Alconna(
#         "群组操作",
#         Subcommand("delete", Args["gid", str], help_text="删除好友"),
#         Subcommand("send", Args["gid", str]["message", str], help_text="发送消息"),
#     )
# )


@_friend_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
):
    try:
        # TODO: 其他adapter的好友api
        fl = await bot.get_friend_list()
        msg = ["{user_id} {nickname}".format_map(g) for g in fl]
        msg = "\n".join(msg)
        msg = f"| UID | 昵称 | 共{len(fl)}个好友\n" + msg
        await Text(msg).send()
        logger.info("查看好友列表", "好友列表", session=session)
    except (ApiNotAvailable, AttributeError) as e:
        await Text("Api未实现...").send()
    except Exception as e:
        logger.error("好友列表发生错误", "好友列表", session=session, e=e)
        await Text("其他未知错误...").send()


@_group_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
):
    try:
        # TODO: 其他adapter的群组api
        gl = await bot.get_group_list()
        msg = ["{group_id} {group_name}".format_map(g) for g in gl]
        msg = "\n".join(msg)
        msg = f"| GID | 名称 | 共{len(gl)}个群组\n" + msg
        await Text(msg).send()
        logger.info("查看群组列表", "群组列表", session=session)
    except (ApiNotAvailable, AttributeError) as e:
        await Text("Api未实现...").send()
    except Exception as e:
        logger.error("查看群组列表发生错误", "群组列表", session=session, e=e)
        await Text("其他未知错误...").send()
