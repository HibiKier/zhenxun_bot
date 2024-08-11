import asyncio
import random

from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import NICKNAME
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.depends import UserName
from zhenxun.utils.message import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="roll",
    description="犹豫不决吗？那就让我帮你决定吧",
    usage="""
    usage：
    随机数字 或 随机选择事件
    指令：
        roll: 随机 0-100 的数字
        roll *[文本]: 随机事件
        示例：roll 吃饭 睡觉 打游戏
    """.strip(),
    extra=PluginExtraData(author="HibiKier", version="0.1").dict(),
)


_matcher = on_command("roll", priority=5, block=True)


@_matcher.handle()
async def _(
    session: EventSession,
    message: UniMsg,
    user_name: str = UserName(),
):
    text = message.extract_plain_text().strip().replace("roll", "", 1).split()
    if not text:
        await MessageUtils.build_message(f"roll: {random.randint(0, 100)}").finish(
            reply_to=True
        )
    await MessageUtils.build_message(
        random.choice(
            [
                "转动命运的齿轮，拨开眼前迷雾...",
                f"启动吧，命运的水晶球，为{user_name}指引方向！",
                "嗯哼，在此刻转动吧！命运！",
                f"在此祈愿，请为{user_name}降下指引...",
            ]
        )
    ).send()
    await asyncio.sleep(1)
    random_text = random.choice(text)
    await MessageUtils.build_message(
        random.choice(
            [
                f"让{NICKNAME}看看是什么结果！答案是：‘{random_text}’",
                f"根据命运的指引，接下来{user_name} ‘{random_text}’ 会比较好",
                f"祈愿被回应了！是 ‘{random_text}’！",
                f"结束了，{user_name}，命运之轮停在了 ‘{random_text}’！",
            ]
        )
    ).send(reply_to=True)
    logger.info(f"发送roll：{text}", "roll", session=session)
