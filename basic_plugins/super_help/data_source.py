from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.utils import get_matchers
from nonebot.adapters.onebot.v11 import Bot
from nonebot import Driver
import asyncio
import nonebot


driver: Driver = nonebot.get_driver()

background = IMAGE_PATH / "background" / "0.png"

superuser_help_image = IMAGE_PATH / "superuser_help.png"


@driver.on_bot_connect
async def create_help_image(bot: Bot = None):
    """
    创建超级用户帮助图片
    """
    await asyncio.get_event_loop().run_in_executor(None, _create_help_image)


def _create_help_image():
    """
    创建管理员帮助图片
    """
    _matchers = get_matchers()
    _plugin_name_list = []
    width = 0
    help_str = "超级用户帮助\n\n*  注: ‘*’ 代表可有多个相同参数 ‘?’ 代表可省略该参数  *\n\n"
    tmp_img = BuildImage(0, 0, plain_text='1', font_size=24)
    for matcher in _matchers:
        plugin_name = ""
        try:
            _plugin = nonebot.plugin.get_plugin(matcher.plugin_name)
            _module = _plugin.module
            try:
                plugin_name = _module.__getattribute__("__zx_plugin_name__")
            except AttributeError:
                continue
            is_superuser_usage = False
            try:
                _ = _module.__getattribute__("__plugin_superuser_usage__")
                is_superuser_usage = True
            except AttributeError:
                pass
            if (
                ("[superuser]" in plugin_name.lower() or is_superuser_usage)
                and plugin_name != "超级用户帮助 [Superuser]"
                and plugin_name not in _plugin_name_list
                and "[hidden]" not in plugin_name.lower()
            ):
                _plugin_name_list.append(plugin_name)
                try:
                    plugin_des = _module.__getattribute__("__plugin_des__")
                except AttributeError:
                    plugin_des = '_'
                plugin_cmd = _module.__getattribute__("__plugin_cmd__")
                if is_superuser_usage:
                    plugin_cmd = [x for x in plugin_cmd if "[_superuser]" in x]
                plugin_cmd = " / ".join(plugin_cmd).replace('[_superuser]', '').strip()
                help_str += f"{plugin_des} -> {plugin_cmd}\n\n"
                x = tmp_img.getsize(f"{plugin_des} -> {plugin_cmd}")[0]
                width = width if width > x else x
        except Exception as e:
            logger.warning(
                f"获取超级用户插件 {matcher.plugin_name}: {plugin_name} 设置失败... {type(e)}：{e}"
            )
    height = len(help_str.split("\n")) * 33
    width += 500
    A = BuildImage(width, height, font_size=24)
    _background = BuildImage(width, height, background=background)
    A.text((300, 140), help_str)
    A.paste(_background, alpha=True)
    A.save(superuser_help_image)
    logger.info(f"已成功加载 {len(_plugin_name_list)} 条超级用户命令")
