import random
from io import BytesIO

from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Args, At, Match, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

__plugin_meta__ = PluginMetadata(
    name="我有一个朋友",
    description="我有一个朋友想问问...",
    usage="""
    指令：
        我有一个朋友想问问 [文本] ?[at]: 当at时你的朋友就是艾特对象
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
    ).dict(),
)

_matcher = on_alconna(
    Alconna("one-friend", Args["text", str]["at?", At]), priority=5, block=True
)

_matcher.shortcut(
    "^我.{0,4}朋友.{0,2}(?:想问问|说|让我问问|想问|让我问|想知道|让我帮他问问|让我帮他问|让我帮忙问|让我帮忙问问|问)(?P<content>.{0,30})$",
    command="one-friend",
    arguments=["{content}"],
    prefix=True,
)


@_matcher.handle()
async def _(bot: Bot, text: str, at: Match[At], session: EventSession):
    gid = session.id3 or session.id2
    if not gid:
        await MessageUtils.build_message("群组id为空...").finish()
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    at_user = None
    if at.available:
        at_user = at.result.target
    user = None
    if at_user:
        user = await PlatformUtils.get_user(bot, at_user, gid)
    else:
        if member_list := await PlatformUtils.get_group_member_list(bot, gid):
            text = text.replace("他", "我").replace("她", "我").replace("它", "我")
            user = random.choice(member_list)
    if user:
        ava_data = None
        if PlatformUtils.get_platform(bot) == "qq":
            ava_data = await PlatformUtils.get_user_avatar(user.user_id, "qq")
        elif user.avatar_url:
            ava_data = (await AsyncHttpx.get(user.avatar_url)).content
        ava_img = BuildImage(200, 100, color=(0, 0, 0, 0))
        if ava_data:
            ava_img = BuildImage(200, 100, background=BytesIO(ava_data))
        await ava_img.circle()
        user_name = "朋友"
        content = BuildImage(400, 30, font_size=30)
        await content.text((0, 0), user_name)
        A = BuildImage(700, 150, font_size=25, color="white")
        await A.paste(ava_img, (30, 25))
        await A.paste(content, (150, 38))
        await A.text((150, 85), text, (125, 125, 125))
        logger.info(f"发送有一个朋友: {text}", "我有一个朋友", session=session)
        await MessageUtils.build_message(A).finish()
    await MessageUtils.build_message("获取用户信息失败...").send()
