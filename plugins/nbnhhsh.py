from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from utils.utils import get_message_text
from services.log import logger
import ujson as json
import aiohttp


__zx_plugin_name__ = "能不能好好说话"
__plugin_usage__ = """
usage：
    说人话
    指令：
        nbnhhsh [文本]
""".strip()
__plugin_des__ = "能不能好好说话，说人话"
__plugin_cmd__ = ["nbnhhsh [文本]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["能不能好好说话", "nbnhhsh"],
}

HHSH_GUESS_URL = "https://lab.magiconch.com/api/nbnhhsh/guess"

nbnhhsh = on_command("nbnhhsh", aliases={"能不能好好说话"}, priority=5, block=True)


@nbnhhsh.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if not msg:
        await nbnhhsh.finish('没话说就别说话！')
    async with aiohttp.ClientSession(
        headers={"content-type": "application/json"}
    ) as session:
        async with session.post(
            HHSH_GUESS_URL, data=json.dumps({"text": msg}), timeout=5
        ) as response:
            if response.status == 200:
                try:
                    data = await response.json()
                    tmp = ""
                    rst = ""
                    for x in data:
                        trans = ""
                        if x.get("trans"):
                            trans = x["trans"][0]
                        elif x.get("inputting"):
                            trans = "，".join(x["inputting"])
                        tmp += f'{x["name"]} -> {trans}\n'
                        rst += trans
                    logger.info(
                        f"(USER {event.user_id}, GROUP "
                        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                        f" 发送能不能好好说话: {msg} -> {rst}"
                    )
                    await nbnhhsh.send(f"{tmp}={rst}", at_sender=True)
                except (IndexError, KeyError):
                    await nbnhhsh.finish("没有找到对应的翻译....")
            else:
                await nbnhhsh.finish("网络访问失败了....")
