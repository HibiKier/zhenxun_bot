import asyncio
from typing import List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from configs.config import Config
from services.log import logger
from utils.depends import ImageList
from utils.manager import group_manager
from utils.message_builder import image

__zx_plugin_name__ = "广播 [Superuser]"
__plugin_usage__ = """
usage：
    指令：
        广播- ?[消息] ?[图片]
        示例：广播- 你们好！
""".strip()
__plugin_des__ = "昭告天下！"
__plugin_cmd__ = ["广播-"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_task__ = {"broadcast": "广播"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_BROADCAST",
    True,
    help_="被动 广播 进群默认开关状态",
    default_value=True,
    type=bool,
)

broadcast = on_command("广播-", priority=1, permission=SUPERUSER, block=True)


@broadcast.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
    arg: Message = CommandArg(),
    img_list: List[str] = ImageList(),
):
    msg = arg.extract_plain_text().strip()
    rst = ""
    for img in img_list:
        rst += image(img)
    gl = [
        g["group_id"]
        for g in await bot.get_group_list()
        if group_manager.check_group_task_status(g["group_id"], "broadcast")
    ]
    g_cnt = len(gl)
    cnt = 0
    error = ""
    x = 0.25
    for g in gl:
        cnt += 1
        if cnt / g_cnt > x:
            await broadcast.send(f"已播报至 {int(cnt / g_cnt * 100)}% 的群聊")
            x += 0.25
        try:
            await bot.send_group_msg(group_id=g, message=msg + rst)
            logger.info(f"投递广播成功", "广播", group_id=g)
        except Exception as e:
            logger.error(f"投递广播失败", "广播", group_id=g, e=e)
            error += f"GROUP {g} 投递广播失败：{type(e)}\n"
        await asyncio.sleep(0.5)
    await broadcast.send(f"已播报至 100% 的群聊")
    if error:
        await broadcast.send(f"播报时错误：{error}")
