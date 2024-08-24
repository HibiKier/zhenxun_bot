import nonebot
from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import At as alcAt
from nonebot_plugin_alconna import Target, Text, UniMsg
from nonebot_plugin_session import EventSession
from nonebot_plugin_userinfo import EventUserInfo, UserInfo

from zhenxun.configs.config import BotConfig
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.group_console import GroupConsole
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

from ._data_source import DialogueManage

__plugin_meta__ = PluginMetadata(
    name="联系管理员",
    description="跨越空间与时间跟管理员对话",
    usage="""
        滴滴滴- ?[文本] ?[图片]
        示例：滴滴滴- 我喜欢你
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        menu_type="联系管理员",
        superuser_help="""
            /t: 查看当前存储的消息
            /t [user_id] [group_id] [文本]: 在group回复指定用户
            /t [user_id] [文本]: 私聊用户
            /t -1 [group_id] [文本]: 在group内发送消息
            /t [id] [文本]: 回复指定id的对话，id在 /t 中获取
            示例：/t 73747222 32848432 你好啊
            示例：/t 73747222 你好不好
            示例：/t -1 32848432 我不太好
            示例：/t 0 我收到你的话了
        """.strip(),
    ).dict(),
)

config = nonebot.get_driver().config


_dialogue_matcher = on_command("滴滴滴-", priority=5, block=True)
_reply_matcher = on_command("/t", priority=1, permission=SUPERUSER, block=True)


@_dialogue_matcher.handle()
async def _(
    bot: Bot,
    message: UniMsg,
    session: EventSession,
    user_info: UserInfo = EventUserInfo(),
):
    if session.id1:
        message[0] = Text(str(message[0]).replace("滴滴滴-", "", 1))
        platform = PlatformUtils.get_platform(bot)
        superuser_id = None
        try:
            if platform:
                superuser_id = BotConfig.get_superuser(platform)
        except IndexError:
            await MessageUtils.build_message("管理员失联啦...").finish()
        if not superuser_id:
            await MessageUtils.build_message("管理员失联啦...").finish()
        uname = user_info.user_displayname or user_info.user_name
        group_name = ""
        gid = session.id3 or session.id2
        if gid:
            if g := await GroupConsole.get(group_id=gid):
                group_name = g.group_name
        logger.info(
            f"发送消息至{platform}管理员: {message}", "滴滴滴-", session=session
        )
        message.insert(0, Text("消息:\n"))
        if gid:
            message.insert(0, Text(f"群组: {group_name}({gid})\n"))
        message.insert(0, Text(f"昵称: {uname}({session.id1})\n"))
        message.insert(0, Text(f"Id: {DialogueManage._index}\n"))
        message.insert(0, Text("*****一份交流报告*****\n"))
        DialogueManage.add(uname, session.id1, gid, group_name, message, platform)
        await message.send(bot=bot, target=Target(superuser_id, private=True))
        await MessageUtils.build_message("已成功发送给管理员啦!").send(reply_to=True)
    else:
        await MessageUtils.build_message("用户id为空...").send()


@_reply_matcher.handle()
async def _(
    bot: Bot,
    message: UniMsg,
    session: EventSession,
):
    message[0] = Text(str(message[0]).replace("/t", "", 1).strip())
    if session.id1:
        msg = message.extract_plain_text()
        if not msg:
            platform = PlatformUtils.get_platform(bot)
            data = DialogueManage._data
            if not data:
                await MessageUtils.build_message("暂无待回复消息...").finish()
            if platform:
                data = [data[d] for d in data if data[d].platform == platform]
                for d in data:
                    await d.message.send(
                        bot=bot, target=Target(session.id1, private=True)
                    )
        else:
            msg = msg.split()
            group_id = ""
            user_id = ""
            if msg[0].replace("-", "", 1).isdigit():
                if len(msg[0]) < 4:
                    _id = int(msg[0])
                    if _id >= 0:
                        if model := DialogueManage.get(_id):
                            user_id = model.user_id
                            group_id = model.group_id
                        else:
                            return MessageUtils.build_message("未获取此id数据").finish()
                        message[0] = Text(" ".join(str(message[0]).split(" ")[1:]))
                    else:
                        user_id = 0
                        if msg[1].isdigit():
                            group_id = msg[1]
                            message[0] = Text(" ".join(str(message[0]).split(" ")[2:]))
                        else:
                            await MessageUtils.build_message("群组id错误...").finish(
                                at_sender=True
                            )
                    DialogueManage.remove(_id)
                else:
                    user_id = msg[0]
                    if msg[1].isdigit() and len(msg[1]) > 5:
                        group_id = msg[1]
                        message[0] = Text(" ".join(str(message[0]).split(" ")[2:]))
                    else:
                        group_id = 0
                        message[0] = Text(" ".join(str(message[0]).split(" ")[1:]))
            else:
                await MessageUtils.build_message("参数错误...").finish(at_sender=True)
            if group_id:
                if user_id:
                    message.insert(0, alcAt("user", user_id))
                    message.insert(1, Text("\n管理员回复\n=======\n"))
                await message.send(Target(group_id), bot)
                await MessageUtils.build_message("消息发送成功!").finish(at_sender=True)
            elif user_id:
                await message.send(Target(user_id, private=True), bot)
                await MessageUtils.build_message("消息发送成功!").finish(at_sender=True)
            else:
                await MessageUtils.build_message("群组id与用户id为空...").send()
    else:
        await MessageUtils.build_message("用户id为空...").send()
