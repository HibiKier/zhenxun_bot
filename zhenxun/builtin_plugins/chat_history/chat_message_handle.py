from datetime import datetime, timedelta

from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Match,
    Option,
    Query,
    on_alconna,
    store_true,
)
from nonebot_plugin_session import EventSession
import pytz

from zhenxun.configs.utils import Command, PluginExtraData
from zhenxun.models.chat_history import ChatHistory
from zhenxun.models.group_member_info import GroupInfoUser
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.image_utils import ImageTemplate
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="消息统计",
    description="消息统计查询",
    usage="""
    格式:
    消息排行 ?[type [日,周,月,年]] ?[--des]

    快捷:
    [日,周,月,年]消息排行 ?[数量]

    示例:
    消息排行             : 所有记录排行
    日消息排行           : 今日记录排行
    周消息排行           : 今日记录排行
    月消息排行           : 今日记录排行
    年消息排行           : 今日记录排行
    消息排行 周 --des    : 逆序周记录排行
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.NORMAL,
        menu_type="数据统计",
        commands=[
            Command(command="消息统计"),
            Command(command="日消息统计"),
            Command(command="周消息排行"),
            Command(command="月消息排行"),
            Command(command="年消息排行"),
        ],
    ).to_dict(),
)


_matcher = on_alconna(
    Alconna(
        "消息排行",
        Option("--des", action=store_true, help_text="逆序"),
        Args["type?", ["日", "周", "月", "年"]]["count?", int, 10],
    ),
    aliases={"消息统计"},
    priority=5,
    block=True,
)

_matcher.shortcut(
    r"(?P<type>['日', '周', '月', '年'])?消息(排行|统计)\s?(?P<cnt>\d+)?",
    command="消息排行",
    arguments=["{type}", "{cnt}"],
    prefix=True,
)


@_matcher.handle()
async def _(
    session: EventSession,
    arparma: Arparma,
    type: Match[str],
    count: Query[int] = Query("count", 10),
):
    group_id = session.id3 or session.id2
    time_now = datetime.now()
    date_scope = None
    zero_today = time_now - timedelta(
        hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second
    )
    date = type.result if type.available else None
    if date:
        if date in ["日"]:
            date_scope = (zero_today, time_now)
        elif date in ["周"]:
            date_scope = (time_now - timedelta(days=7), time_now)
        elif date in ["月"]:
            date_scope = (time_now - timedelta(days=30), time_now)
    column_name = ["名次", "昵称", "发言次数"]
    if rank_data := await ChatHistory.get_group_msg_rank(
        group_id, count.result, "DES" if arparma.find("des") else "DESC", date_scope
    ):
        idx = 1
        data_list = []
        for uid, num in rank_data:
            if user := await GroupInfoUser.filter(
                user_id=uid, group_id=group_id
            ).first():
                user_name = user.user_name
            else:
                user_name = uid
            data_list.append([idx, user_name, num])
            idx += 1
        if not date_scope:
            if date_scope := await ChatHistory.get_group_first_msg_datetime(group_id):
                date_scope = date_scope.astimezone(
                    pytz.timezone("Asia/Shanghai")
                ).replace(microsecond=0)
            else:
                date_scope = time_now.replace(microsecond=0)
            date_str = f"{str(date_scope).split('+')[0]} - 至今"
        else:
            date_str = (
                f"{date_scope[0].replace(microsecond=0)} - "
                f"{date_scope[1].replace(microsecond=0)}"
            )
        A = await ImageTemplate.table_page(
            f"消息排行({count.result})", date_str, column_name, data_list
        )
        logger.info(
            f"查看消息排行 数量={count.result}", arparma.header_result, session=session
        )
        await MessageUtils.build_message(A).finish(reply_to=True)
    await MessageUtils.build_message("群组消息记录为空...").finish()


# # @test.handle()
# # async def _(event: MessageEvent):
# #     print(await ChatHistory.get_user_msg(event.user_id, "private"))
# #     print(await ChatHistory.get_user_msg_count(event.user_id, "private"))
# #     print(await ChatHistory.get_user_msg(event.user_id, "group"))
# #     print(await ChatHistory.get_user_msg_count(event.user_id, "group"))
# #     print(await ChatHistory.get_group_msg(event.group_id))
# #     print(await ChatHistory.get_group_msg_count(event.group_id))
