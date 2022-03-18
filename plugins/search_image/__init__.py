from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.typing import T_State
from services.log import logger
from utils.utils import get_message_img
from utils.message_builder import custom_forward_msg
from nonebot.params import CommandArg, Arg, ArgStr, Depends
from .saucenao import get_saucenao_image


__zx_plugin_name__ = "识图"
__plugin_usage__ = """
usage：
    识别图片 [二次元图片]
    指令：
        识图 [图片]
""".strip()
__plugin_des__ = "以图搜图，看破本源"
__plugin_cmd__ = ["识图"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["识图"],
}
__plugin_configs__ = {
    "MAX_FIND_IMAGE_COUNT": {"value": 3, "help": "识图返回的最大结果数", "default_value": 3},
    "API_KEY": {
        "value": None,
        "help": "Saucenao的API_KEY，通过 https://saucenao.com/user.php?page=search-api 注册获取",
    },
}


search_image = on_command("识图", block=True, priority=5)


async def get_image_info(mod: str, url: str):
    if mod == "saucenao":
        return await get_saucenao_image(url)


def parse_image(key: str):
    async def _key_parser(
        state: T_State, img: Message = Arg(key)
    ):
        if not get_message_img(img):
            await search_image.reject_arg(key, "请发送要识别的图片！")
        state[key] = img
    return _key_parser


@search_image.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if msg:
        state["mod"] = msg
    else:
        state["mod"] = "saucenao"
    if get_message_img(event.json()):
        state["img"] = event.message


@search_image.got("img", prompt="图来！", parameterless=[Depends(parse_image("img"))])
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    mod: str = ArgStr("mod"),
    img: Message = Arg("img"),
):
    img = get_message_img(img)[0]
    await search_image.send("开始处理图片...")
    msg = await get_image_info(mod, img)
    if isinstance(msg, str):
        await search_image.finish(msg, at_sender=True)
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_forward_msg(
            group_id=event.group_id, messages=custom_forward_msg(msg, bot.self_id)
        )
    else:
        for m in msg[1:]:
            await search_image.send(m)
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 识图:" + img
    )
