from nonebot import require
from fastapi import APIRouter

from ....base_model import Result
from .data_source import BotManage
from ....utils import authentication

require("plugin_store")

router = APIRouter(prefix="/dashboard")


@router.get(
    "/get_bot_list",
    dependencies=[authentication()],
    deprecated="获取bot列表",  # type: ignore
)
async def _() -> Result:
    try:
        return Result.ok(await BotManage.get_bot_list(), "拿到信息啦!")
    except Exception as e:
        return Result.fail(f"发生了一点错误捏 {type(e)}: {e}")
