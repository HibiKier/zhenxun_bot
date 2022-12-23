import nonebot
from configs.path_config import IMAGE_PATH
from nonebot import Driver
from services.log import logger
from utils.image_template import help_template
from utils.image_utils import (BuildImage, build_sort_image, group_image,
                               text2image)
from utils.manager import group_manager, plugin_data_manager
from utils.manager.models import PluginType

driver: Driver = nonebot.get_driver()

background = IMAGE_PATH / "background" / "0.png"

ADMIN_HELP_IMAGE = IMAGE_PATH / "admin_help_img.png"


@driver.on_bot_connect
async def init_task():
    if not group_manager.get_task_data():
        group_manager.load_task()
        logger.info(f"已成功加载 {len(group_manager.get_task_data())} 个被动技能.")


async def create_help_image():
    """
    创建管理员帮助图片
    """
    await _create_help_image()


async def _create_help_image():
    """
    创建管理员帮助图片
    """
    if ADMIN_HELP_IMAGE.exists():
        return
    plugin_data_ = plugin_data_manager.get_data()
    image_list = []
    task_list = []
    for plugin_data in [plugin_data_[x] for x in plugin_data_]:
        try:
            usage = None
            if plugin_data.plugin_type == PluginType.ADMIN and plugin_data.usage:
                usage = await text2image(
                    plugin_data.usage, padding=5, color=(204, 196, 151)
                )
            if usage:
                await usage.acircle_corner()
                level = 5
                if plugin_data.plugin_setting:
                    level = plugin_data.plugin_setting.level or level
                image = await help_template(plugin_data.name + f"[{level}]", usage)
                image_list.append(image)
            if plugin_data.task:
                for x in plugin_data.task.keys():
                    task_list.append(plugin_data.task[x])
        except Exception as e:
            logger.warning(
                f"获取群管理员插件 {plugin_data.model}: {plugin_data.name} 设置失败... {type(e)}：{e}"
            )
    task_str = "\n".join(task_list)
    task_str = "通过 开启/关闭 来控制群被动\n----------\n" + task_str
    task_image = await text2image(task_str, padding=5, color=(204, 196, 151))
    task_image = await help_template("被动任务", task_image)
    image_list.append(task_image)
    image_group, _ = group_image(image_list)
    A = await build_sort_image(image_group, color="#f9f6f2", padding_top=180)
    await A.apaste(
        BuildImage(0, 0, font="CJGaoDeGuo.otf", plain_text="群管理员帮助", font_size=50),
        (50, 30),
        True,
    )
    await A.apaste(
        BuildImage(
            0,
            0,
            font="CJGaoDeGuo.otf",
            plain_text="注: ‘*’ 代表可有多个相同参数 ‘?’ 代表可省略该参数",
            font_size=30,
            font_color="red",
        ),
        (50, 90),
        True,
    )
    await A.asave(ADMIN_HELP_IMAGE)
    logger.info(f"已成功加载 {len(image_list)} 条管理员命令")
