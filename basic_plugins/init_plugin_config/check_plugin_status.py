from utils.manager import plugins_manager
from nonebot.adapters.onebot.v11 import Bot


async def check_plugin_status(bot: Bot):
    """
    遍历查看插件加载情况
    """
    rst = ""
    for plugin in plugins_manager.keys():
        data = plugins_manager.get(plugin)
        if data.get("error") or data.get("error") is None:
            rst += f'{plugin}:{data["plugin_name"]}\n'
    if rst:
        rst = "以下插件加载失败..\n" + rst
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]), message=rst[:-1]
        )
