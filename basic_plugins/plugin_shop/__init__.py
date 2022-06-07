from nonebot import on_command, on_regex

from .data_source import show_plugin_repo, install_plugin, uninstall_plugin, download_json
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.params import CommandArg

from utils.message_builder import image
from nonebot.permission import SUPERUSER


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
__plugin_cmd__ = [""]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"

show_repo = on_regex("^查看插件仓库$", priority=1, block=True, permission=SUPERUSER)

update_repo = on_regex("^更新插件仓库$", priority=1, block=True, permission=SUPERUSER)

install_plugin_matcher = on_command("安装插件", priority=1, block=True, permission=SUPERUSER)

uninstall_plugin_matcher = on_command("卸载插件", priority=1, block=True, permission=SUPERUSER)


@install_plugin_matcher.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    msg = await install_plugin(arg)
    await install_plugin_matcher.send(msg)


@uninstall_plugin_matcher.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    msg = await uninstall_plugin(arg)
    await install_plugin_matcher.send(msg)


@update_repo.handle()
async def _(bot: Bot, event: MessageEvent):
    code = await download_json()
    if code == 200:
        await update_repo.finish("更新插件仓库信息成功！")
    await update_repo.send("更新插件仓库信息失败！")
    

@show_repo.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = await show_plugin_repo()
    if isinstance(msg, int):
        await show_repo.finish("文件下载失败或解压失败..")
    await show_repo.send(image(b64=msg))
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 查看插件仓库"
    )

