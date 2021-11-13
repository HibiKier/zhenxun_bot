from asyncio.exceptions import TimeoutError

import aiofiles
import aiohttp
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message, GroupMessageEvent
from nonebot.typing import T_State

from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.message_builder import image
from utils.utils import get_message_text, is_number
from utils.manager import withdraw_message_manager

try:
    import ujson as json
except ModuleNotFoundError:
    import json


__zx_plugin_name__ = "pid搜索"
__plugin_usage__ = """
usage：
    通过 pid 搜索图片
    指令：
        p搜 [pid]
""".strip()
__plugin_des__ = "通过 pid 搜索图片"
__plugin_cmd__ = ["p搜 [pid]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["p搜"],
}

pid_search = on_command("p搜", aliases={"pixiv搜", "P搜"}, priority=5, block=True)

url = "https://api.fantasyzone.cc/tu/search.php"


@pid_search.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pid = get_message_text(event.json())
    if pid:
        if pid in ["取消", "算了"]:
            await pid_search.finish("已取消操作...")
        if not is_number(pid):
            await pid_search.reject("笨蛋，重新输入数！字！", at_sender=True)
        state["pid"] = pid


@pid_search.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pid = get_message_text(event.json())
    if pid:
        state["pid"] = pid


@pid_search.got("pid", prompt="需要查询的图片PID是？")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pid = state["pid"]
    params = {
        "id": pid,
        "p": 1,
    }
    async with aiohttp.ClientSession() as session:
        for _ in range(10):
            try:
                async with session.get(url, timeout=2, params=params) as response:
                    data = json.loads(await response.text())
            except TimeoutError:
                pass
            else:
                if not data["width"] and not data["height"]:
                    await pid_search.finish(f"没有搜索到 PID：{pid} 的图片", at_sender=True)
                pid = data["id"]
                title = data["title"]
                author = data["userName"]
                author_id = data["userId"]
                img_url = data["url"]
                for _ in range(5):
                    try:
                        await download_pic(img_url, event.user_id)
                    except TimeoutError:
                        pass
                    else:
                        break
                else:
                    await pid_search.finish("图片下载失败了....", at_sender=True)
                tmp = ""
                if isinstance(event, GroupMessageEvent):
                    tmp = "\n【注】将在30后撤回......"
                msg_id = await pid_search.send(
                    Message(
                        f"title：{title}\n"
                        f"pid：{pid}\n"
                        f"author：{author}\n"
                        f"author_id：{author_id}\n"
                        f'{image(f"pid_search_{event.user_id}.png", "temp")}'
                        f"{tmp}"
                    )
                )
                logger.info(
                    f"(USER {event.user_id}, "
                    f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                    f" 查询图片 PID：{pid}"
                )
                if isinstance(event, GroupMessageEvent):
                    withdraw_message_manager.append((msg_id, 30))
                break
        else:
            await pid_search.finish("图片下载失败了....", at_sender=True)


async def download_pic(img_url: str, user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url, timeout=2) as res:
            async with aiofiles.open(
                    f"{IMAGE_PATH}/temp/pid_search_{user_id}.png", "wb"
            ) as f:
                await f.write(await res.read())
