from configs.config import Config
import nonebot


Config.add_plugin_config(
    "image_management",
    "IMAGE_DIR_LIST",
    ["美图", "萝莉", "壁纸"],
    name="图库操作",
    help_="公开图库列表，可自定义添加 [如果含有send_setu插件，请不要添加色图库]",
    default_value=[],
)

Config.add_plugin_config(
    "image_management",
    "WITHDRAW_IMAGE_MESSAGE",
    (0, 1),
    name="图库操作",
    help_="自动撤回，参1：延迟撤回发送图库图片的时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
    default_value=(0, 1),
)

Config.add_plugin_config(
    "image_management:delete_img",
    "DELETE_IMAGE_LEVEL [LEVEL]",
    7,
    help_="删除图库图片需要的管理员等级",
    default_value=7,
)

Config.add_plugin_config(
    "image_management:move_img",
    "MOVE_IMAGE_LEVEL [LEVEL]",
    7,
    help_="移动图库图片需要的管理员等级",
    default_value=7,
)

Config.add_plugin_config(
    "image_management:upload_img",
    "UPLOAD_IMAGE_LEVEL [LEVEL]",
    6,
    help_="上传图库图片需要的管理员等级",
    default_value=6,
)


nonebot.load_plugins("plugins/image_management")
