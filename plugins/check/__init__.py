from nonebot import on_command
from .data_source import Check
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from utils.message_builder import image


__zx_plugin_name__ = "服务器自我检查 [Superuser]"
__plugin_usage__ = """
usage：
    查看服务器当前状态
    指令：
        自检
"""
__plugin_des__ = "查看服务器当前状态"
__plugin_cmd__ = ["自检/check"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"


check = Check()


check_ = on_command(
    "自检", aliases={"check"}, rule=to_me(), permission=SUPERUSER, block=True, priority=1
)


@check_.handle()
async def _():
    await check_.send(image(b64=await check.show()))
