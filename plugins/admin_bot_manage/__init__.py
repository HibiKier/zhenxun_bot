from nonebot import on_command
from util.utils import get_message_text, get_message_imgs, scheduler, get_bot
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from .data_source import set_group_status, custom_group_welcome, change_group_switch, \
    update_member_info, group_current_status
from nonebot.adapters.cqhttp.permission import GROUP
from services.log import logger
from configs.config import plugins2name_dict
from nonebot.plugin import export

__plugin_name__ = '自定义进群欢迎消息'

__plugin_usage__ = '''自定义进群欢迎消息 [消息] [图片](可省略)
    \t示例：自定义进群欢迎消息 欢迎新人！[图片]'''

export = export()
export.update_member_info = update_member_info

cmds = []
for cmd_list in plugins2name_dict.values():
    for cmd in cmd_list:
        cmds.append(f'开启{cmd}')
        cmds.append(f'关闭{cmd}')
cmds = set(cmds)

group_status = on_command('oc_reminds', aliases={'开启早晚安', '关闭早晚安',
                                                 '开启进群欢迎', '关闭进群欢迎',
                                                 '开启每日开箱重置提醒', '关闭每日开箱重置提醒',
                                                 '开启b站转发解析', '关闭b站转发解析',
                                                 '开启epic通知', '关闭epic通知',
                                                 '开启丢人爬', '关闭丢人爬',
                                                 '开启原神黄历提醒', '关闭原神黄历提醒',
                                                 '开启全部通知', '开启所有通知', '关闭全部通知', '关闭所有通知',
                                                 '群通知状态'}, permission=GROUP, priority=1, block=True)

switch_rule = on_command('switch_rule', aliases=cmds, permission=GROUP, priority=4, block=True)
custom_welcome = on_command('自定义进群欢迎消息', aliases={'自定义欢迎消息', '自定义群欢迎消息'}, permission=GROUP, priority=5, block=True)
refresh_member_group = on_command("更新群组成员列表", aliases={"更新群组成员信息"}, permission=GROUP, priority=5, block=True)


@switch_rule.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await switch_rule.send(await change_group_switch(state["_prefix"]["raw_command"].strip(), event.group_id))
    logger.info(f'USER {event.user_id} GROUP {event.group_id} 使用群功能管理命令 {state["_prefix"]["raw_command"]}')


@group_status.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if state["_prefix"]["raw_command"] in ['群通知状态']:
        await group_status.finish(await group_current_status(event.group_id))
    await group_status.send(await set_group_status(state["_prefix"]["raw_command"], event.group_id),
                            at_sender=True)
    logger.info(f'USER {event.user_id} GROUP {event.group_id} 使用群通知管理命令 {state["_prefix"]["raw_command"]}')


@custom_welcome.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    if not msg and not imgs:
        await custom_welcome.finish('格式：自定义群欢迎消息 [文本] [图片]\n\t示例：自定义群欢迎消息 我们都是萝莉控，你呢？ [图片]')
    await custom_welcome.finish(await custom_group_welcome(msg, imgs, event.user_id, event.group_id), at_sender=True)


@refresh_member_group.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    if await update_member_info(event.group_id):
        await refresh_member_group.finish("更新群员信息成功！", at_sender=True)
    else:
        await refresh_member_group.finish("更新群员信息失败！", at_sender=True)


# 自动更新群员信息
@scheduler.scheduled_job(
    'cron',
    hour=2,
    minute=1,
)
async def _():
    bot = get_bot()
    gl = await bot.get_group_list(self_id=bot.self_id)
    gl = [g['group_id'] for g in gl]
    for g in gl:
        try:
            await update_member_info(g)
            logger.info(f'更新群组 g:{g} 成功')
        except Exception as e:
            logger.error(f'更新群组错误 g:{g} e:{e}')
