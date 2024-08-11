from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot_plugin_alconna import Alconna, Args, Arparma, Match, UniMessage, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.message import MessageUtils

from ._data_source import ImageManagementManage

base_config = Config.get("image_management")

__plugin_meta__ = PluginMetadata(
    name="移动图片",
    description="图库间的图片移动操作",
    usage="""
    指令：
        移动图片 [源图库] [目标图库] [id]
        查看图库
        示例：移动图片 萝莉 美图 234
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.ADMIN,
        admin_level=base_config.get("MOVE_IMAGE_LEVEL"),
    ).dict(),
)


_matcher = on_alconna(
    Alconna("移动图片", Args["source?", str]["destination?", str]["index?", str]),
    rule=to_me(),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    source: Match[str],
    destination: Match[str],
    index: Match[str],
    state: T_State,
):
    image_dir_list = base_config.get("IMAGE_DIR_LIST")
    if not image_dir_list:
        await MessageUtils.build_message("未发现任何图库").finish()
    _text = ""
    for i, dir in enumerate(image_dir_list):
        _text += f"{i}. {dir}\n"
    state["dir_list"] = _text[:-1]
    if source.available:
        _matcher.set_path_arg("source", source.result)
    if destination.available:
        _matcher.set_path_arg("destination", destination.result)
    if index.available:
        _matcher.set_path_arg("index", index.result)


@_matcher.got_path(
    "source",
    prompt=UniMessage.template(
        "要从哪个图库移出？【发送'取消', '算了'来取消操作】\n{dir_list}"
    ),
)
async def _(source: str):
    if source in ["取消", "算了"]:
        await MessageUtils.build_message("已取消操作...").finish()
    image_dir_list = base_config.get("IMAGE_DIR_LIST")
    if source.isdigit():
        index = int(source)
        if index <= len(image_dir_list) - 1:
            name = image_dir_list[index]
    if name not in image_dir_list:
        await _matcher.reject_path("source", "此目录不正确，请重新输入目录！")
    _matcher.set_path_arg("source", name)


@_matcher.got_path(
    "destination",
    prompt=UniMessage.template(
        "要移动到哪个图库？【发送'取消', '算了'来取消操作】\n{dir_list}"
    ),
)
async def _(destination: str):
    if destination in ["取消", "算了"]:
        await MessageUtils.build_message("已取消操作...").finish()
    image_dir_list = base_config.get("IMAGE_DIR_LIST")
    name = None
    if destination.isdigit():
        index = int(destination)
        if index <= len(image_dir_list) - 1:
            name = image_dir_list[index]
    if name not in image_dir_list:
        await _matcher.reject_path("destination", "此目录不正确，请重新输入目录！")
    _matcher.set_path_arg("destination", name)


@_matcher.got_path("index", "要移动的图片id是？【发送'取消', '算了'来取消操作】")
async def _(
    session: EventSession,
    arparma: Arparma,
    index: str,
):
    if index in ["取消", "算了"]:
        await MessageUtils.build_message("已取消操作...").finish()
    if not index.isdigit():
        await _matcher.reject_path("index", "图片id需要输入数字...")
    source = _matcher.get_path_arg("source", None)
    destination = _matcher.get_path_arg("destination", None)
    if not source:
        await MessageUtils.build_message("转出图库名称为空...").finish()
    if not destination:
        await MessageUtils.build_message("转入图库名称为空...").finish()
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if file_name := await ImageManagementManage.move_image(
        source, destination, int(index), session.id1, session.platform
    ):
        logger.info(
            f"移动图片成功 图库: {source} -> {destination} --- 名称: {file_name}",
            arparma.header_result,
            session=session,
        )
        await MessageUtils.build_message(
            f"移动图片成功!\n图库: {source} -> {destination}"
        ).finish()
    await MessageUtils.build_message("图片删除失败...").finish()
