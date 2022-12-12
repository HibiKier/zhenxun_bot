
from ._utils import HelpImageBuild
from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
from utils.manager import (
    plugins2settings_manager,
    admin_manager,
)
from typing import Optional
import nonebot


random_bk_path = IMAGE_PATH / "background" / "help" / "simple_help"

background = IMAGE_PATH / "background" / "0.png"


async def create_help_img(group_id: Optional[int]):
    """
    生成帮助图片
    :param group_id: 群号
    """
    await HelpImageBuild().build_image(group_id)


def get_plugin_help(msg: str, is_super: bool = False) -> Optional[str]:
    """
    获取功能的帮助信息
    :param msg: 功能cmd
    :param is_super: 是否为超级用户
    """
    module = plugins2settings_manager.get_plugin_module(
        msg
    ) or admin_manager.get_plugin_module(msg)
    if module:
        try:
            plugin = nonebot.plugin.get_plugin(module)
            metadata = plugin.metadata
            if plugin:
                if is_super:
                    result = plugin.module.__getattribute__(
                        "__plugin_superuser_usage__"
                    )
                else:
                    result = (
                        metadata.usage
                        if metadata
                        else plugin.module.__getattribute__("__plugin_usage__")
                    )
                if result:
                    width = 0
                    for x in result.split("\n"):
                        _width = len(x) * 24
                        width = width if width > _width else _width
                    height = len(result.split("\n")) * 45
                    A = BuildImage(width, height, font_size=24)
                    bk = BuildImage(
                        width,
                        height,
                        background=IMAGE_PATH / "background" / "1.png",
                    )
                    A.paste(bk, alpha=True)
                    A.text((int(width * 0.048), int(height * 0.21)), result)
                    return A.pic2bs4()
        except AttributeError:
            pass
    return None
