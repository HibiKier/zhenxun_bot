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
    name="删除图片",
    description="不好看的图片删掉删掉！",
    usage="""
    指令：
        删除图片 [图库] [id]
        查看图库
        示例：删除图片 美图 666
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.ADMIN,
        admin_level=base_config.get("DELETE_IMAGE_LEVEL"),
    ).dict(),
)


_matcher = on_alconna(
    Alconna("删除图片", Args["name?", str]["index?", str]),
    rule=to_me(),
    priority=5,
    block=True,
)


@_matcher.handle()
async def _(
    name: Match[str],
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
    if name.available:
        _matcher.set_path_arg("name", name.result)
    if index.available:
        _matcher.set_path_arg("index", index.result)


@_matcher.got_path(
    "name",
    prompt=UniMessage.template(
        "请输入要删除的目标图库(id 或 名称)【发送'取消', '算了'来取消操作】\n{dir_list}"
    ),
)
async def _(name: str):
    if name in ["取消", "算了"]:
        await MessageUtils.build_message("已取消操作...").finish()
    image_dir_list = base_config.get("IMAGE_DIR_LIST")
    if name.isdigit():
        index = int(name)
        if index <= len(image_dir_list) - 1:
            name = image_dir_list[index]
    if name not in image_dir_list:
        await _matcher.reject_path("name", "此目录不正确，请重新输入目录！")
    _matcher.set_path_arg("name", name)


@_matcher.got_path("index", "请输入要删除的图片id？【发送'取消', '算了'来取消操作】")
async def _(
    session: EventSession,
    arparma: Arparma,
    index: str,
):
    if index in ["取消", "算了"]:
        await MessageUtils.build_message("已取消操作...").finish()
    if not index.isdigit():
        await _matcher.reject_path("index", "图片id需要输入数字...")
    name = _matcher.get_path_arg("name", None)
    if not name:
        await MessageUtils.build_message("图库名称为空...").finish()
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if file_name := await ImageManagementManage.delete_image(
        name, int(index), session.id1, session.platform
    ):
        logger.info(
            f"删除图片成功 图库: {name} --- 名称: {file_name}",
            arparma.header_result,
            session=session,
        )
        await MessageUtils.build_message(
            f"删除图片成功!\n图库: {name}\n名称: {index}.jpg"
        ).finish()
    await MessageUtils.build_message("图片删除失败...").finish()
