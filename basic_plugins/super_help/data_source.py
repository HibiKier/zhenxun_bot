import nonebot
from nonebot import Driver

from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.image_template import help_template
from utils.image_utils import BuildImage, build_sort_image, group_image, text2image
from utils.manager import plugin_data_manager
from utils.manager.models import PluginType

driver: Driver = nonebot.get_driver()

SUPERUSER_HELP_IMAGE = IMAGE_PATH / "superuser_help.png"


@driver.on_bot_connect
async def create_help_image():
    """
    创建超级用户帮助图片
    """
    if SUPERUSER_HELP_IMAGE.exists():
        return
    plugin_data_ = plugin_data_manager.get_data()
    image_list = []
    task_list = []
    for plugin_data in [
        plugin_data_[x]
        for x in plugin_data_
        if plugin_data_[x].name != "超级用户帮助 [Superuser]"
    ]:
        try:
            if plugin_data.plugin_type in [PluginType.SUPERUSER, PluginType.ADMIN]:
                usage = None
                if (
                    plugin_data.plugin_type == PluginType.SUPERUSER
                    and plugin_data.usage
                ):
                    usage = await text2image(
                        plugin_data.usage, padding=5, color=(204, 196, 151)
                    )
                if plugin_data.superuser_usage:
                    usage = await text2image(
                        plugin_data.superuser_usage, padding=5, color=(204, 196, 151)
                    )
                if usage:
                    await usage.acircle_corner()
                    image = await help_template(plugin_data.name, usage)
                    image_list.append(image)
            if plugin_data.task:
                for x in plugin_data.task.keys():
                    task_list.append(plugin_data.task[x])
        except Exception as e:
            logger.warning(
                f"获取超级用户插件 {plugin_data.model}: {plugin_data.name} 设置失败...", e=e
            )
    task_str = "\n".join(task_list)
    task_str = "通过私聊 开启被动/关闭被动 + [被动名称] 来控制全局被动\n----------\n" + task_str
    task_image = await text2image(task_str, padding=5, color=(204, 196, 151))
    task_image = await help_template("被动任务", task_image)
    image_list.append(task_image)
    image_group, _ = group_image(image_list)
    A = await build_sort_image(image_group, color="#f9f6f2", padding_top=180)
    await A.apaste(
        BuildImage(0, 0, font="CJGaoDeGuo.otf", plain_text="超级用户帮助", font_size=50),
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
    await A.asave(SUPERUSER_HELP_IMAGE)
    logger.info(f"已成功加载 {len(image_list)} 条超级用户命令")
