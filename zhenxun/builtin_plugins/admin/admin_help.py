import nonebot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, Arparma, on_alconna
from nonebot_plugin_alconna.matcher import AlconnaMatcher
from nonebot_plugin_saa import Image, Text
from nonebot_plugin_session import EventSession

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.task_info import TaskInfo
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType
from zhenxun.utils.exception import EmptyError
from zhenxun.utils.image_utils import (
    BuildImage,
    build_sort_image,
    group_image,
    text2image,
)
from zhenxun.utils.rules import admin_check, ensure_group

__plugin_meta__ = PluginMetadata(
    name="群组管理员帮助",
    description="管理员帮助列表",
    usage="""
    管理员帮助
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.ADMIN,
        admin_level=1,
    ).dict(),
)

_matcher = on_alconna(
    Alconna("管理员帮助"),
    rule=admin_check(1) & ensure_group,
    priority=5,
    block=True,
)


ADMIN_HELP_IMAGE = IMAGE_PATH / "ADMIN_HELP.png"
if ADMIN_HELP_IMAGE.exists():
    ADMIN_HELP_IMAGE.unlink()


async def build_help() -> BuildImage:
    """构造管理员帮助图片

    异常:
        EmptyError: 管理员帮助为空

    返回:
        BuildImage: 管理员帮助图片
    """
    plugin_list = await PluginInfo.filter(
        plugin_type__in=[PluginType.ADMIN, PluginType.SUPER_AND_ADMIN]
    ).all()
    data_list = []
    for plugin in plugin_list:
        if _plugin := nonebot.get_plugin_by_module_name(plugin.module_path):
            if _plugin.metadata:
                data_list.append({"plugin": plugin, "metadata": _plugin.metadata})
    font = BuildImage.load_font("HYWenHei-85W.ttf", 20)
    image_list = []
    for data in data_list:
        plugin = data["plugin"]
        metadata = data["metadata"]
        try:
            usage = None
            description = None
            if metadata.usage:
                usage = await text2image(
                    metadata.usage,
                    padding=5,
                    color=(255, 255, 255),
                    font_color=(0, 0, 0),
                )
            if metadata.description:
                description = await text2image(
                    metadata.description,
                    padding=5,
                    color=(255, 255, 255),
                    font_color=(0, 0, 0),
                )
            width = 0
            height = 100
            if usage:
                width = usage.width
                height += usage.height
            if description and description.width > width:
                width = description.width
                height += description.height
            font_width, font_height = BuildImage.get_text_size(
                plugin.name + f"[{plugin.level}]", font
            )
            if font_width > width:
                width = font_width
            A = BuildImage(width + 30, height + 120, "#EAEDF2")
            await A.text((15, 10), plugin.name + f"[{plugin.level}]")
            await A.text((15, 70), "简介:")
            if not description:
                description = BuildImage(A.width - 30, 30, (255, 255, 255))
            await description.circle_corner(10)
            await A.paste(description, (15, 100))
            if not usage:
                usage = BuildImage(A.width - 30, 30, (255, 255, 255))
            await usage.circle_corner(10)
            await A.text((15, description.height + 115), "用法:")
            await A.paste(usage, (15, description.height + 145))
            await A.circle_corner(10)
            image_list.append(A)
        except Exception as e:
            logger.warning(
                f"获取群管理员插件 {plugin.module}: {plugin.name} 设置失败...",
                "管理员帮助",
                e=e,
            )
    if task_list := await TaskInfo.all():
        task_str = "\n".join([task.name for task in task_list])
        task_str = "通过 开启/关闭群被动 来控制群被动\n----------\n" + task_str
        task_image = await text2image(task_str, padding=5, color=(255, 255, 255))
        await task_image.circle_corner(10)
        A = BuildImage(task_image.width + 50, task_image.height + 85, "#EAEDF2")
        await A.text((25, 10), "被动技能")
        await A.paste(task_image, (25, 50))
        await A.circle_corner(10)
        image_list.append(A)
    if not image_list:
        raise EmptyError()
    image_group, _ = group_image(image_list)
    A = await build_sort_image(image_group, color=(255, 255, 255), padding_top=160)
    text = await BuildImage.build_text_image(
        "群管理员帮助",
        size=40,
    )
    tip = await BuildImage.build_text_image(
        "注: ‘*’ 代表可有多个相同参数 ‘?’ 代表可省略该参数", size=25, font_color="red"
    )
    await A.paste(text, (50, 30))
    await A.paste(tip, (50, 90))
    await A.save(ADMIN_HELP_IMAGE)
    return BuildImage(1, 1)


@_matcher.handle()
async def _(
    session: EventSession,
    matcher: AlconnaMatcher,
    arparma: Arparma,
):
    if not ADMIN_HELP_IMAGE.exists():
        try:
            await build_help()
        except EmptyError:
            await Text("管理员帮助为空").finish(reply=True)
    await Image(ADMIN_HELP_IMAGE).send()
    logger.info("查看管理员帮助", arparma.header_result, session=session)
