from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from utils.http_utils import AsyncHttpx
from services.log import logger
import ujson as json


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
async def _(event: MessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if not msg:
        await nbnhhsh.finish("没话说就别说话！")
    response = await AsyncHttpx.post(
        HHSH_GUESS_URL,
        data=json.dumps({"text": msg}),
        timeout=5,
        headers={"content-type": "application/json"},
    )
    try:
        data = response.json()
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
