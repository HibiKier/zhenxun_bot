from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from services.log import logger
from ._data_source import get_data, gen_wbtop_pic
from utils.utils import is_number
from configs.path_config import IMAGE_PATH
from utils.http_utils import AsyncPlaywright
import asyncio

__zx_plugin_name__ = "微博热搜"
__plugin_usage__ = """
usage：
    在QQ上吃个瓜
    指令：
        微博热搜：发送实时热搜
        微博热搜 [id]：截图该热搜页面
        示例：微博热搜 5
""".strip()
__plugin_des__ = "刚买完瓜，在吃瓜现场"
__plugin_cmd__ = ["微博热搜", "微博热搜 [id]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["微博热搜"],
}

wbtop = on_command("wbtop", aliases={"微博热搜"}, priority=5, block=True)


wbtop_url = "https://v2.alapi.cn/api/new/wbtop"

wbtop_data = []


@wbtop.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    global wbtop_data
    msg = arg.extract_plain_text().strip()
    if not wbtop_data or not msg:
        data, code = await get_data(wbtop_url)
        if code != 200:
            await wbtop.finish(data, at_sender=True)
        wbtop_data = data["data"]
        if not msg:
            img = await asyncio.get_event_loop().run_in_executor(
                None, gen_wbtop_pic, wbtop_data
            )
            await wbtop.send(img)
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 查询微博热搜"
            )
    if is_number(msg) and 0 < int(msg) <= 50:
        url = wbtop_data[int(msg) - 1]["url"]
        try:
            await wbtop.send("开始截取数据...")
            img = await AsyncPlaywright.screenshot(
                url,
                f"{IMAGE_PATH}/temp/wbtop_{event.user_id}.png",
                "#pl_feedlist_index",
                sleep=5
            )
            await wbtop.send(img)
        except Exception as e:
            logger.error(f"微博热搜截图出错... {type(e)}: {e}")
            await wbtop.send("发生了一些错误.....")
