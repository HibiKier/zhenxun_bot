from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.utils import get_matchers
from utils.manager import group_manager
from nonebot.adapters.onebot.v11 import Bot
from nonebot import Driver
import asyncio
import nonebot


driver: Driver = nonebot.get_driver()

background = IMAGE_PATH / "background" / "0.png"

admin_help_image = IMAGE_PATH / 'admin_help_img.png'


@driver.on_bot_connect
async def init_task(bot: Bot = None):
    if not group_manager.get_task_data():
        await group_manager.init_group_task()
        logger.info(f'已成功加载 {len(group_manager.get_task_data())} 个被动技能.')


async def create_help_image():
    """
    创建管理员帮助图片
    """
    await asyncio.get_event_loop().run_in_executor(
        None, _create_help_image
    )


def _create_help_image():
    """
    创建管理员帮助图片
    """
    _matchers = get_matchers()
    _plugin_name_list = []
    width = 0
    _plugin_level = {}
    for matcher in _matchers:
        _plugin = nonebot.plugin.get_plugin(matcher.plugin_name)
        _module = _plugin.module
        try:
            plugin_name = _module.__getattribute__("__zx_plugin_name__")
        except AttributeError:
            continue
        try:
            if (
                "[admin]" in plugin_name.lower()
                and plugin_name not in _plugin_name_list
                and plugin_name != "管理帮助 [Admin]"
            ):
                _plugin_name_list.append(plugin_name)
                plugin_settings = _module.__getattribute__("__plugin_settings__")
                plugin_des = _module.__getattribute__("__plugin_des__")
                plugin_cmd = _module.__getattribute__("__plugin_cmd__")
                plugin_cmd = [x for x in plugin_cmd if "[_superuser]" not in x]
                admin_level = int(plugin_settings["admin_level"])
                if _plugin_level.get(admin_level):
                    _plugin_level[admin_level].append(
                        f"[{admin_level}] {plugin_des} -> " + " / ".join(plugin_cmd)
                    )
                else:
                    _plugin_level[admin_level] = [
                        f"[{admin_level}] {plugin_des} -> " + " / ".join(plugin_cmd)
                    ]
                x = len(f"[{admin_level}] {plugin_des} -> " + " / ".join(plugin_cmd)) * 23
                width = width if width > x else x
        except AttributeError:
            logger.warning(f"获取管理插件 {matcher.plugin_name}: {plugin_name} 设置失败...")
    help_str = "*  注: ‘*’ 代表可有多个相同参数 ‘?’ 代表可省略该参数  *\n\n" \
               "[权限等级] 管理员帮助：\n\n"
    x = list(_plugin_level.keys())
    x.sort()
    for level in x:
        for help_ in _plugin_level[level]:
            help_str += f"\t{help_}\n\n"
    help_str += '-----[被动技能开关]-----\n\n'
    task_data = group_manager.get_task_data()
    for i, x in enumerate(task_data.keys()):
        help_str += f'{i+1}.开启/关闭{task_data[x]}\n\n'
    height = len(help_str.split("\n")) * 33
    A = BuildImage(width, height, font_size=24)
    _background = BuildImage(width, height, background=background)
    A.text((150, 110), help_str)
    A.paste(_background, alpha=True)
    A.save(admin_help_image)
    logger.info(f'已成功加载 {len(_plugin_name_list)} 条管理员命令')


