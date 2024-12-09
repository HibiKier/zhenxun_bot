from typing import Any

from nonebot.internal.params import Depends
from nonebot.matcher import Matcher
from nonebot.params import Command
from nonebot_plugin_session import EventSession
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.config import Config
from zhenxun.utils.message import MessageUtils


def CheckUg(check_user: bool = True, check_group: bool = True):
    """检测群组id和用户id是否存在

    参数:
        check_user: 检查用户id.
        check_group: 检查群组id.
    """

    async def dependency(session: EventSession):
        if check_user:
            user_id = session.id1
            if not user_id:
                await MessageUtils.build_message("用户id为空").finish()
        if check_group:
            group_id = session.id3 or session.id2
            if not group_id:
                await MessageUtils.build_message("群组id为空").finish()

    return Depends(dependency)


def OneCommand():
    """
    获取单个命令Command
    """

    async def dependency(
        cmd: tuple[str, ...] = Command(),
    ):
        return cmd[0] if cmd else None

    return Depends(dependency)


def UserName():
    """
    用户名称
    """

    async def dependency(user_info: Uninfo):
        return user_info.user.nick or user_info.user.name or ""

    return Depends(dependency)


def GetConfig(
    module: str | None = None,
    config: str = "",
    default_value: Any = None,
    prompt: str | None = None,
):
    """获取配置项

    参数:
        module: 模块名，为空时默认使用当前插件模块名
        config: 配置项名称
        default_value: 默认值
        prompt: 为空时提示
    """

    async def dependency(matcher: Matcher):
        module_ = module or matcher.plugin_name
        if module_:
            value = Config.get_config(module_, config, default_value)
            if value is None and prompt:
                # await matcher.finish(prompt or f"配置项 {config} 未填写！")
                await matcher.finish(prompt)
            return value

    return Depends(dependency)


def CheckConfig(
    module: str | None = None,
    config: str | list[str] = "",
    prompt: str | None = None,
):
    """检测配置项在配置文件中是否填写

    参数:
        module: 模块名，为空时默认使用当前插件模块名
        config: 需要检查的配置项名称
        prompt: 为空时提示
    """

    async def dependency(matcher: Matcher):
        module_ = module or matcher.plugin_name
        if module_:
            config_list = [config] if isinstance(config, str) else config
            for c in config_list:
                if Config.get_config(module_, c) is None:
                    await matcher.finish(prompt or f"配置项 {c} 未填写！")

    return Depends(dependency)
