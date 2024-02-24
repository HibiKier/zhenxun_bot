import nonebot

from zhenxun.configs.path_config import IMAGE_PATH
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.utils.image_utils import BuildImage

from ._utils import HelpImageBuild

random_bk_path = IMAGE_PATH / "background" / "help" / "simple_help"

background = IMAGE_PATH / "background" / "0.png"


async def create_help_img(group_id: int | None):
    """
    说明:
        生成帮助图片
    参数:
        :param group_id: 群号
    """
    await HelpImageBuild().build_image(group_id)


async def get_plugin_help(name: str) -> str:
    """获取功能的帮助信息

    参数:
        name: 插件名称
    """
    if plugin := await PluginInfo.get_or_none(name=name):
        _plugin = nonebot.get_plugin_by_module_name(plugin.module_path)
        if _plugin and _plugin.metadata:
            return _plugin.metadata.usage
        return "糟糕! 该功能没有帮助喔..."
    return "没有查找到这个功能噢..."
