from nonebot import require
from fastapi import APIRouter

from .model import PluginIr
from ....base_model import Result
from ....utils import authentication

require("plugin_store")
from zhenxun.builtin_plugins.plugin_store import ShopManage

router = APIRouter(prefix="/store")


@router.get(
    "/get_plugin_store",
    dependencies=[authentication()],
    deprecated="获取插件商店插件信息",  # type: ignore
)
async def _() -> Result:
    try:
        data = await ShopManage.get_data()
        return Result.ok(data)
    except Exception as e:
        return Result.fail(f"获取插件商店插件信息失败: {type(e)}: {e}")


@router.post(
    "/install_plugin",
    dependencies=[authentication()],
    deprecated="安装插件",  # type: ignore
)
async def _(param: PluginIr) -> Result:
    try:
        result = await ShopManage.add_plugin(param.id)  # type: ignore
        return Result.ok(result)
    except Exception as e:
        return Result.fail(f"安装插件失败: {type(e)}: {e}")


@router.post(
    "/remove_plugin",
    dependencies=[authentication()],
    deprecated="移除插件",  # type: ignore
)
async def _(param: PluginIr) -> Result:
    try:
        result = await ShopManage.remove_plugin(param.id)  # type: ignore
        return Result.ok(result)
    except Exception as e:
        return Result.fail(f"移除插件失败: {type(e)}: {e}")
