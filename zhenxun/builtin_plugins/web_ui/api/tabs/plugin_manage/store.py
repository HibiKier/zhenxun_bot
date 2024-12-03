from nonebot import require
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from zhenxun.models.plugin_info import PluginInfo

from .model import PluginIr
from ....base_model import Result
from ....utils import authentication

router = APIRouter(prefix="/store")


@router.get(
    "/get_plugin_store",
    dependencies=[authentication()],
    response_model=Result[dict],
    response_class=JSONResponse,
    deprecated="获取插件商店插件信息",  # type: ignore
)
async def _() -> Result[dict]:
    try:
        require("plugin_store")
        from zhenxun.builtin_plugins.plugin_store import ShopManage

        data = await ShopManage.get_data()
        plugin_list = [
            {**data[name].dict(), "name": name, "id": idx}
            for idx, name in enumerate(data)
        ]
        modules = await PluginInfo.filter(load_status=True).values_list(
            "module", flat=True
        )
        return Result.ok({"install_module": modules, "plugin_list": plugin_list})
    except Exception as e:
        return Result.fail(f"获取插件商店插件信息失败: {type(e)}: {e}")


@router.post(
    "/install_plugin",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    deprecated="安装插件",  # type: ignore
)
async def _(param: PluginIr) -> Result:
    try:
        require("plugin_store")
        from zhenxun.builtin_plugins.plugin_store import ShopManage

        result = await ShopManage.add_plugin(param.id)  # type: ignore
        return Result.ok(info=result)
    except Exception as e:
        return Result.fail(f"安装插件失败: {type(e)}: {e}")


@router.post(
    "/update_plugin",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    deprecated="更新插件",  # type: ignore
)
async def _(param: PluginIr) -> Result:
    try:
        require("plugin_store")
        from zhenxun.builtin_plugins.plugin_store import ShopManage

        result = await ShopManage.update_plugin(param.id)  # type: ignore
        return Result.ok(info=result)
    except Exception as e:
        return Result.fail(f"更新插件失败: {type(e)}: {e}")


@router.post(
    "/remove_plugin",
    dependencies=[authentication()],
    response_model=Result,
    response_class=JSONResponse,
    deprecated="移除插件",  # type: ignore
)
async def _(param: PluginIr) -> Result:
    try:
        require("plugin_store")
        from zhenxun.builtin_plugins.plugin_store import ShopManage

        result = await ShopManage.remove_plugin(param.id)  # type: ignore
        return Result.ok(info=result)
    except Exception as e:
        return Result.fail(f"移除插件失败: {type(e)}: {e}")
