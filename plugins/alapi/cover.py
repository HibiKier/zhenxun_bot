from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Message, GroupMessageEvent
from utils.message_builder import image
from nonebot.params import CommandArg
from ._data_source import get_data
from services.log import logger

__zx_plugin_name__ = "b封面"
__plugin_usage__ = """
usage：
    b封面 [链接/av/bv/cv/直播id]
    示例：b封面 av86863038
""".strip()
__plugin_des__ = "快捷的b站视频封面获取方式"
__plugin_cmd__ = ["b封面/B封面"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["b封面", "B封面"],
}


cover = on_command("b封面", aliases={"B封面"}, priority=5, block=True)


cover_url = "https://v2.alapi.cn/api/bilibili/cover"


@cover.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    params = {"c": msg}
    data, code = await get_data(cover_url, params)
    if code != 200:
        await cover.finish(data, at_sender=True)
    data = data["data"]
    title = data["title"]
    img = data["cover"]
    await cover.send(Message(f"title：{title}\n{image(img)}"))
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 获取b站封面: {title} url：{img}"
    )
