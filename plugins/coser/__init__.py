from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from services.log import logger
from asyncio.exceptions import TimeoutError
from utils.message_builder import image
from configs.path_config import IMAGE_PATH
from utils.utils import get_local_proxy
import aiohttp
import aiofiles

__zx_plugin_name__ = "coser"
__plugin_usage__ = """
usage：
    三次元也不戳，嘿嘿嘿
    指令：
        cos/coser
""".strip()
__plugin_des__ = "三次元也不戳，嘿嘿嘿"
__plugin_cmd__ = ["cos/coser"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["cos", "coser", "括丝", "COS", "Cos", "cOS", "coS"],
}

coser = on_command(
    "cos", aliases={"coser", "括丝", "COS", "Cos", "cOS", "coS"}, priority=5, block=True
)


url = "http://ovooa.com/API/cosplay/api.php"


@coser.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    async with aiohttp.ClientSession() as session:
        try:
            for _ in range(3):
                try:
                    async with session.get(url, proxy=get_local_proxy(), timeout=2) as response:
                        _url = (await response.json())['text']
                        async with session.get(
                            _url, timeout=5, proxy=get_local_proxy(), verify_ssl=False
                        ) as res:
                            if res.status == 200:
                                async with aiofiles.open(
                                    f"{IMAGE_PATH}/temp/{event.user_id}_coser.jpg", "wb"
                                ) as f:
                                    await f.write(await res.read())
                                logger.info(
                                    f"(USER {event.user_id}, "
                                    f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                                    f" 发送COSER"
                                )
                                await coser.send(
                                    image(f"{event.user_id}_coser.jpg", "temp")
                                )
                                break
                except (TimeoutError, KeyError):
                    pass
            else:
                await coser.send("你cos给我看！")
        except Exception as e:
            await coser.send("发生了预料之外的错误..请稍后再试或联系管理员修复...")
            logger.error(f"coser 发送了未知错误 {type(e)}：{e}")
