from fastapi import APIRouter, WebSocket
from loguru import logger
from nonebot.utils import escape_tag
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from .log_manager import LOG_STORAGE

router = APIRouter()


@router.get("/logs", response_model=list[str])
async def system_logs_history(reverse: bool = False):
    """历史日志

    参数:
        reverse: 反转顺序.
    """
    return LOG_STORAGE.list(reverse=reverse)  # type: ignore


@router.websocket("/logs")
async def system_logs_realtime(websocket: WebSocket):
    await websocket.accept()

    async def log_listener(log: str):
        await websocket.send_text(log)

    LOG_STORAGE.listeners.add(log_listener)
    try:
        while websocket.client_state == WebSocketState.CONNECTED:
            recv = await websocket.receive()
            logger.trace(
                f"{system_logs_realtime.__name__!r} received "
                f"<e>{escape_tag(repr(recv))}</e>"
            )
    except WebSocketDisconnect:
        pass
    finally:
        LOG_STORAGE.listeners.remove(log_listener)
    return
