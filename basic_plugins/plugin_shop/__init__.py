from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from services.log import logger
from utils.message_builder import image

from .data_source import (
    download_json,
    install_plugin,
    show_plugin_repo,
    uninstall_plugin,
)

__zx_plugin_name__ = "插件商店 [Superuser]"
__plugin_usage__ = """
usage：
    下载安装插件
    指令：
        查看插件仓库
        更新插件仓库
        安装插件 [name/id] （重新安装等同于更新）
        卸载插件 [name/id]
""".strip()
__plugin_des__ = "从真寻适配仓库中下载插件"
__plugin_cmd__ = ["查看插件仓库", "更新插件仓库", "安装插件 [name/id]", "卸载插件 [name/id]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"

show_repo = on_regex("^查看插件仓库$", priority=1, block=True, permission=SUPERUSER)

update_repo = on_regex("^更新插件仓库$", priority=1, block=True, permission=SUPERUSER)

install_plugin_matcher = on_command(
    "安装插件", priority=1, block=True, permission=SUPERUSER
)

uninstall_plugin_matcher = on_command(
    "卸载插件", priority=1, block=True, permission=SUPERUSER
)


@install_plugin_matcher.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    name = arg.extract_plain_text().strip()
    msg = await install_plugin(name)
    await install_plugin_matcher.send(msg)
    logger.info(f"安装插件: {name}", "安装插件", event.user_id)


@uninstall_plugin_matcher.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    name = arg.extract_plain_text().strip()
    msg = await uninstall_plugin(name)
    await install_plugin_matcher.send(msg)
    logger.info(f"卸载插件: {name}", "卸载插件", event.user_id)


@update_repo.handle()
async def _(bot: Bot, event: MessageEvent):
    code = await download_json()
    if code == 200:
        await update_repo.finish("更新插件仓库信息成功！")
    await update_repo.send("更新插件仓库信息失败！")
    logger.info("更新插件仓库信息", "更新插件仓库信息", event.user_id)


@show_repo.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = await show_plugin_repo()
    if isinstance(msg, int):
        await show_repo.finish("文件下载失败或解压失败..")
    await show_repo.send(image(msg))
    logger.info("查看插件仓库", "查看插件仓库", event.user_id)
