from .group_user_checkin import group_user_check_in, group_user_check, group_impression_rank
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from util.utils import get_message_text
from nonebot.plugin import MatcherGroup


__plugin_name__ = '签到'
__plugin_usage__ = (
    '用法：\n'
    '对我说 “签到” 来签到\n'
    '“我的签到” 来获取历史签到信息\n'
    '“好感度排行” 来查看当前好感度前十的伙伴\n'
    '/ 签到时有 3% 概率 * 2 /'

)


sign_match_group = MatcherGroup(priority=5, permission=GROUP, block=True)

sign = sign_match_group.on_command("签到")


@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await sign.send(
        await group_user_check_in(event.user_id, event.group_id),
        at_sender=True,
    )


my_sign = sign_match_group.on_command(cmd="我的签到", aliases={'好感度'})


@my_sign.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await my_sign.send(
        await group_user_check(event.user_id, event.group_id),
        at_sender=True,
    )

sign_ranking = sign_match_group.on_command(cmd="积分排行", aliases={'好感度排行', '签到排行', '积分排行', '好感排行',
                                                               '好感度排名，签到排名，积分排名'})


@sign_ranking.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await sign_ranking.send(
        await group_impression_rank(event.group_id)
    )