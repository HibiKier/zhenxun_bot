import os
import platform
from pathlib import Path

import nonebot
from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.params import ArgStr
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import NICKNAME
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils

__plugin_meta__ = PluginMetadata(
    name="重启",
    description="执行脚本重启真寻",
    usage=f"""
    重启
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier", version="0.1", plugin_type=PluginType.SUPERUSER
    ).dict(),
)


_matcher = on_command(
    "重启",
    permission=SUPERUSER,
    rule=to_me(),
    priority=1,
    block=True,
)

driver = nonebot.get_driver()


RESTART_MARK = Path() / "is_restart"

RESTART_FILE = Path() / "restart.sh"


@_matcher.got(
    "flag",
    prompt=f"确定是否重启{NICKNAME}？确定请回复[是|好|确定]（重启失败咱们将失去联系，请谨慎！）",
)
async def _(bot: Bot, session: EventSession, flag: str = ArgStr("flag")):
    if flag.lower() in ["true", "是", "好", "确定", "确定是"]:
        await MessageUtils.build_message(f"开始重启{NICKNAME}..请稍等...").send()
        with open(RESTART_MARK, "w", encoding="utf8") as f:
            f.write(f"{bot.self_id} {session.id1}")
        logger.info("开始重启真寻...", "重启", session=session)
        if str(platform.system()).lower() == "windows":
            import sys

            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            os.system("./restart.sh")
    else:
        await MessageUtils.build_message("已取消操作...").send()


@driver.on_bot_connect
async def _(bot: Bot):
    if str(platform.system()).lower() != "windows":
        if not RESTART_FILE.exists():
            with open(RESTART_FILE, "w", encoding="utf8") as f:
                f.write(
                    f"pid=$(netstat -tunlp | grep "
                    + str(bot.config.port)
                    + " | awk '{print $7}')\n"
                    "pid=${pid%/*}\n"
                    "kill -9 $pid\n"
                    "sleep 3\n"
                    "python3 bot.py"
                )
            os.system("chmod +x ./restart.sh")
            logger.info(
                "已自动生成 restart.sh(重启) 文件，请检查脚本是否与本地指令符合..."
            )
    if RESTART_MARK.exists():
        with open(RESTART_MARK, "r", encoding="utf8") as f:
            bot_id, session_id = f.read().split()
        if bot := nonebot.get_bot(bot_id):
            if target := PlatformUtils.get_target(bot, session_id):
                await MessageUtils.build_message(f"{NICKNAME}已成功重启！").send(
                    target, bot=bot
                )
        RESTART_MARK.unlink()
