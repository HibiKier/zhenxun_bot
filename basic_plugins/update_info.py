from nonebot import on_command
from utils.message_builder import image


__zx_plugin_name__ = "更新信息"
__plugin_usage__ = """
usage：
    更新信息
    指令：
        更新信息
""".strip()
__plugin_des__ = "当前版本的更新信息"
__plugin_cmd__ = ["更新信息"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["更新信息"],
}


update_info = on_command("更新信息", aliases={"更新日志"}, priority=5, block=True)


@update_info.handle()
async def _():
    img = image("update_info.png")
    if img:
        await update_info.finish(image("update_info.png"))
    else:
        await update_info.finish("目前没有更新信息哦")
