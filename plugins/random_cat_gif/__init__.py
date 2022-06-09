from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import Event
from utils.http_utils import AsyncHttpx

__zx_plugin_name__ = "来个猫猫"
__plugin_usage__ = """
usage：
来个猫猫
""".strip()
__plugin_des__ = "来个猫猫"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["来个猫猫"]
__plugin_version__ = 0.1
__plugin_author__ = "yajiwa & Copaan"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["来个猫猫"],
}

miao = on_command("来个猫猫", block=True, priority=5)


@miao.handle()
async def hf(bot: Bot, ev: Event):
    try:
        img = await AsyncHttpx().get("http://edgecats.net/")
    except:
        return await bot.send(event=ev, message="获取猫猫图片超时")
    await bot.send(event=ev, message=MessageSegment.image(img.content))
