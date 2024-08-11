from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot_plugin_alconna import Alconna, Args, Arparma
from nonebot_plugin_alconna import Image as alcImage
from nonebot_plugin_alconna import Match, UniMessage, UniMsg, image_fetch, on_alconna
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.message import MessageUtils

from ._data_source import ImageManagementManage

base_config = Config.get("image_management")

__plugin_meta__ = PluginMetadata(
    name="上传图片",
    description="上传图片至指定图库",
    usage="""
    指令：
        查看图库
        上传图片 [图库] [图片]
        示例：上传图片 美图 [图片]
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.ADMIN,
        admin_level=base_config.get("UPLOAD_IMAGE_LEVEL"),
    ).dict(),
)


_upload_matcher = on_alconna(
    Alconna("上传图片", Args["name?", str]["img?", alcImage]),
    rule=to_me(),
    priority=5,
    block=True,
)

_continuous_upload_matcher = on_alconna(
    Alconna("连续上传图片", Args["name?", str]),
    rule=to_me(),
    priority=5,
    block=True,
)

_show_matcher = on_alconna(Alconna("查看公开图库"), priority=1, block=True)


@_show_matcher.handle()
async def _():
    image_dir_list = base_config.get("IMAGE_DIR_LIST")
    if not image_dir_list:
        await MessageUtils.build_message("未发现任何图库").finish()
    text = "公开图库列表：\n"
    for i, e in enumerate(image_dir_list):
        text += f"\t{i+1}.{e}\n"
    await MessageUtils.build_message(text[:-1]).send()


@_upload_matcher.handle()
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    name: Match[str],
    img: Match[bytes],
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
        _upload_matcher.set_path_arg("name", name.result)
    if img.available:
        result = await AsyncHttpx.get(img.result.url)  # type: ignore
        _upload_matcher.set_path_arg("img", result.content)


@_continuous_upload_matcher.handle()
async def _(bot: Bot, state: T_State, name: Match[str]):
    image_dir_list = base_config.get("IMAGE_DIR_LIST")
    if not image_dir_list:
        await MessageUtils.build_message("未发现任何图库").finish()
    _text = ""
    for i, dir in enumerate(image_dir_list):
        _text += f"{i}. {dir}\n"
    state["dir_list"] = _text[:-1]
    if name.available:
        _upload_matcher.set_path_arg("name", name.result)


@_continuous_upload_matcher.got_path(
    "name",
    prompt=UniMessage.template(
        "请选择要上传的图库(id 或 名称)【发送'取消', '算了'来取消操作】\n{dir_list}"
    ),
)
@_upload_matcher.got_path(
    "name",
    prompt=UniMessage.template(
        "请选择要上传的图库(id 或 名称)【发送'取消', '算了'来取消操作】\n{dir_list}"
    ),
)
async def _(name: str, state: T_State):
    if name in ["取消", "算了"]:
        await MessageUtils.build_message("已取消操作...").finish()
    image_dir_list = base_config.get("IMAGE_DIR_LIST")
    if name.isdigit():
        index = int(name)
        if index <= len(image_dir_list) - 1:
            name = image_dir_list[index]
    if name not in image_dir_list:
        await _upload_matcher.reject_path("name", "此目录不正确，请重新输入目录！")
    _upload_matcher.set_path_arg("name", name)


@_upload_matcher.got_path("img", "图呢图呢图呢图呢！GKD！", image_fetch)
async def _(
    bot: Bot,
    session: EventSession,
    arparma: Arparma,
    img: bytes,
):
    name = _upload_matcher.get_path_arg("name", None)
    if not name:
        await MessageUtils.build_message("图库名称为空...").finish()
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if file_name := await ImageManagementManage.upload_image(
        img, name, session.id1, session.platform
    ):
        logger.info(
            f"图库: {name} --- 名称: {file_name}",
            arparma.header_result,
            session=session,
        )
        await MessageUtils.build_message(
            f"上传图片成功!\n图库: {name}\n名称: {file_name}"
        ).finish()
    await MessageUtils.build_message("图片上传失败...").finish()


@_continuous_upload_matcher.got(
    "img", "图呢图呢图呢图呢！GKD！【在最后一张图片中+‘stop’为停止】"
)
async def _(
    bot: Bot,
    arparma: Arparma,
    session: EventSession,
    state: T_State,
    message: UniMsg,
):
    name = _continuous_upload_matcher.get_path_arg("name", None)
    if not name:
        await MessageUtils.build_message("图库名称为空...").finish()
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if not state.get("img_list"):
        state["img_list"] = []
    msg = message.extract_plain_text().strip().replace(arparma.header_result, "", 1)
    if msg in ["取消", "算了"]:
        await MessageUtils.build_message("已取消操作...").finish()
    if msg != "stop":
        for msg in message:
            if isinstance(msg, alcImage):
                state["img_list"].append(msg.url)
        await _continuous_upload_matcher.reject("图再来！！【发送‘stop’为停止】")
    if state["img_list"]:
        await MessageUtils.build_message("正在下载, 请稍后...").send()
        file_list = []
        for img in state["img_list"]:
            if file_name := await ImageManagementManage.upload_image(
                img, name, session.id1, session.platform
            ):
                file_list.append(img)
                logger.info(
                    f"图库: {name} --- 名称: {file_name}",
                    "上传图片",
                    session=session,
                )
        await MessageUtils.build_message(
            f"上传图片成功!共上传了{len(file_list)}张图片\n图库: {name}\n名称: {', '.join(file_list)}"
        ).finish()
    await MessageUtils.build_message("图片上传失败...").finish()
