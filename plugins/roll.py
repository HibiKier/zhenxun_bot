from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from utils.utils import get_message_text
from services.log import logger
from configs.config import NICKNAME
import random
import asyncio

__plugin_name__ = "roll"
__plugin_usage__ = (
    "用法：\n" "\troll -> 随机数字\n" "\troll *[文本] -> 决定事件\n" "示例：roll 吃饭 睡觉 打游戏"
)


roll = on_command("roll", priority=5, block=True)


@roll.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json()).split()
    if not msg:
        await roll.finish(f"roll: {random.randint(0, 100)}", at_sender=True)
    user_name = event.sender.card if event.sender.card else event.sender.nickname
    await roll.send(
        random.choice(
            [
                "转动命运的齿轮，拨开眼前迷雾...",
                f"启动吧，命运的水晶球，为{user_name}指引方向！",
                "嗯哼，在此刻转动吧！命运！",
                f"在此祈愿，请为{user_name}降下指引...",
            ]
        )
    )
    await asyncio.sleep(1)
    x = random.choice(msg)
    await roll.send(
        random.choice(
            [
                f"让{NICKNAME}看看是什么结果！答案是：‘{x}’",
                f"根据命运的指引，接下来{user_name} ‘{x}’ 会比较好",
                f"祈愿被回应了！是 ‘{x}’！",
                f"结束了，{user_name}，命运之轮停在了 ‘{x}’！",
            ]
        )
    )
    logger.info(
        f"(USER {event.user_id}, "
        f"GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送roll：{msg}"
    )
