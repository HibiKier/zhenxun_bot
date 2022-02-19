from nonebot import on_regex
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
from ._data_source import get_data
from services.log import logger

__zx_plugin_name__ = "网易云热评"
__plugin_usage__ = """
usage：
    到点了，还是防不了下塔
    指令：
        网易云热评/到点了/12点了
""".strip()
__plugin_des__ = "生了个人，我很抱歉"
__plugin_cmd__ = ["网易云热评", "到点了", "12点了"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["网易云热评", "网易云评论", "到点了", "12点了"],
}


comments_163 = on_regex(
    "^(网易云热评|网易云评论|到点了|12点了)$", priority=5, block=True
)


comments_163_url = "https://v2.alapi.cn/api/comment"


@comments_163.handle()
async def _(event: MessageEvent):
    data, code = await get_data(comments_163_url)
    if code != 200:
        await comments_163.finish(data, at_sender=True)
    data = data["data"]
    comment = data["comment_content"]
    song_name = data["title"]
    await comments_163.send(f"{comment}\n\t——《{song_name}》")
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 发送网易云热评: {comment} \n\t\t————{song_name}"
    )
