from configs.path_config import IMAGE_PATH
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from utils.message_builder import image
from services.log import logger
from utils.image_utils import BuildImage
from nonebot.params import CommandArg

__zx_plugin_name__ = "鲁迅说"
__plugin_usage__ = """
usage：
    鲁迅说了啥？
    指令：
        鲁迅说 [文本]
""".strip()
__plugin_des__ = "鲁迅说他没说过这话！"
__plugin_cmd__ = ["鲁迅说"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["鲁迅说"],
}
__plugin_block_limit__ = {
    "rst": "你的鲁迅正在说，等会"
}

luxun = on_command("鲁迅说过", aliases={"鲁迅说"}, priority=5, block=True)


luxun_author = BuildImage(0, 0, plain_text="--鲁迅", font_size=30, font='msyh.ttf', font_color=(255, 255, 255))


@luxun.handle()
async def handle(state: T_State, arg: Message = CommandArg()):
    args = arg.extract_plain_text().strip()
    if args:
        state["content"] = args if args else "烦了，不说了"


@luxun.got("content", prompt="你让鲁迅说点啥?")
async def handle_event(event: MessageEvent, state: T_State):
    content = state["content"].strip()
    if content.startswith(",") or content.startswith("，"):
        content = content[1:]
    A = BuildImage(0, 0, font_size=37, background=f'{IMAGE_PATH}/other/luxun.jpg', font='msyh.ttf')
    x = ""
    if len(content) > 40:
        await luxun.finish('太长了，鲁迅说不完...')
    while A.getsize(content)[0] > A.w - 50:
        n = int(len(content) / 2)
        x += content[:n] + '\n'
        content = content[n:]
    x += content
    if len(x.split('\n')) > 2:
        await luxun.finish('太长了，鲁迅说不完...')
    A.text((int((480 - A.getsize(x.split("\n")[0])[0]) / 2), 300), x, (255, 255, 255))
    A.paste(luxun_author, (320, 400), True)
    await luxun.send(image(b64=A.pic2bs4()))
    logger.info(
        f"USER {event.user_id} GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'} 鲁迅说过 {content}"
    )
