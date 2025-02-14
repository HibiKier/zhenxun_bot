from nonebot.plugin import PluginMetadata
from PIL.ImageFont import FreeTypeFont

from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.task_info import TaskInfo
from zhenxun.services.log import logger
from zhenxun.utils._build_image import BuildImage
from zhenxun.utils.image_utils import build_sort_image, group_image, text2image

from .config import ADMIN_HELP_IMAGE
from .utils import get_plugins


async def build_usage_des_image(
    metadata: PluginMetadata,
) -> tuple[BuildImage | None, BuildImage | None]:
    """构建用法和描述图片

    参数:
        metadata: PluginMetadata

    返回:
        tuple[BuildImage | None, BuildImage | None]: 用法和描述图片
    """
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
    return usage, description


async def build_image(
    plugin: PluginInfo, metadata: PluginMetadata, font: FreeTypeFont
) -> BuildImage:
    """构建帮助图片

    参数:
        plugin: PluginInfo
        metadata: PluginMetadata
        font: FreeTypeFont

    返回:
        BuildImage: 帮助图片

    """
    usage, description = await build_usage_des_image(metadata)
    width = 0
    height = 100
    if usage:
        width = usage.width
        height += usage.height
    if description and description.width > width:
        width = description.width
        height += description.height
    font_width, _ = BuildImage.get_text_size(f"{plugin.name}[{plugin.level}]", font)
    if font_width > width:
        width = font_width
    A = BuildImage(width + 30, height + 120, "#EAEDF2")
    await A.text((15, 10), f"{plugin.name}[{plugin.level}]")
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
    return A


async def build_help():
    """构造管理员帮助图片

    返回:
        BuildImage: 管理员帮助图片
    """
    font = BuildImage.load_font("HYWenHei-85W.ttf", 20)
    image_list = []
    for data in await get_plugins():
        plugin = data.plugin
        metadata = data.metadata
        try:
            A = await build_image(plugin, metadata, font)
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
