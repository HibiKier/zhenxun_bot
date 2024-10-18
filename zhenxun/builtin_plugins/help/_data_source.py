import nonebot
from nonebot_plugin_uninfo import Uninfo

from zhenxun.utils.enum import PluginType
from zhenxun.models.level_user import LevelUser
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.utils.image_utils import BuildImage, ImageTemplate

from .html_help import build_html_image
from .normal_help import build_normal_image
from .zhenxun_help import build_zhenxun_image
from ._config import GROUP_HELP_PATH, SIMPLE_HELP_IMAGE, base_config

random_bk_path = IMAGE_PATH / "background" / "help" / "simple_help"

background = IMAGE_PATH / "background" / "0.png"


driver = nonebot.get_driver()


async def create_help_img(session: Uninfo, group_id: str | None):
    """生成帮助图片

    参数:
        session: Uninfo
        group_id: 群号
    """
    help_type: str = base_config.get("type")
    if help_type.lower() == "html":
        result = BuildImage.open(await build_html_image(group_id))
    elif help_type.lower() == "zhenxun":
        result = BuildImage.open(await build_zhenxun_image(session, group_id))
    else:
        result = await build_normal_image(group_id)
    if group_id:
        await result.save(GROUP_HELP_PATH / f"{group_id}.png")
    else:
        await result.save(SIMPLE_HELP_IMAGE)


async def get_user_allow_help(user_id: str) -> list[PluginType]:
    """获取用户可访问插件类型列表

    参数:
        user_id: 用户id

    返回:
        list[PluginType]: 插件类型列表
    """
    type_list = [PluginType.NORMAL, PluginType.DEPENDANT]
    for level in await LevelUser.filter(user_id=user_id).values_list(
        "user_level", flat=True
    ):
        if level > 0:  # type: ignore
            type_list.extend((PluginType.ADMIN, PluginType.SUPER_AND_ADMIN))
            break
    if user_id in driver.config.superusers:
        type_list.append(PluginType.SUPERUSER)
    return type_list


async def get_plugin_help(
    user_id: str, name: str, is_superuser: bool
) -> str | BuildImage:
    """获取功能的帮助信息

    参数:
        user_id: 用户id
        name: 插件名称或id
        is_superuser: 是否为超级用户
    """
    type_list = await get_user_allow_help(user_id)
    if name.isdigit():
        plugin = await PluginInfo.get_or_none(id=int(name), plugin_type__in=type_list)
    else:
        plugin = await PluginInfo.get_or_none(
            name__iexact=name, load_status=True, plugin_type__in=type_list
        )
    if plugin:
        _plugin = nonebot.get_plugin_by_module_name(plugin.module_path)
        if _plugin and _plugin.metadata:
            items = None
            if is_superuser:
                extra = _plugin.metadata.extra
                if usage := extra.get("superuser_help"):
                    items = {
                        "简介": _plugin.metadata.description,
                        "用法": usage,
                    }
            else:
                items = {
                    "简介": _plugin.metadata.description,
                    "用法": _plugin.metadata.usage,
                }
            if items:
                return await ImageTemplate.hl_page(plugin.name, items)
        return "糟糕! 该功能没有帮助喔..."
    return "没有查找到这个功能噢..."
