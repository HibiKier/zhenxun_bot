import nonebot
from fastapi import APIRouter
from nonebot import on_message
from nonebot_plugin_session import EventSession
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot_plugin_alconna import At, Text, Hyper, Image, UniMsg
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect

from zhenxun.utils.depends import UserName
from zhenxun.models.group_member_info import GroupInfoUser

from ....config import AVA_URL
from .model import Message, MessageItem

driver = nonebot.get_driver()

ws_conn: WebSocket | None = None

ID2NAME = {}

ID_LIST = []

ws_router = APIRouter()


matcher = on_message(block=False, priority=1, rule=lambda: bool(ws_conn))


@driver.on_shutdown
async def _():
    if ws_conn:
        await ws_conn.close()


@ws_router.websocket("/chat")
async def _(websocket: WebSocket):
    global ws_conn
    await websocket.accept()
    if not ws_conn:
        ws_conn = websocket
        try:
            while websocket.client_state == WebSocketState.CONNECTED:
                await websocket.receive()
        except WebSocketDisconnect:
            ws_conn = None


async def message_handle(
    message: UniMsg,
    group_id: str | None,
):
    messages = []
    for m in message:
        if isinstance(m, Text | str):
            messages.append(MessageItem(type="text", msg=str(m)))
        elif isinstance(m, Image):
            if m.url:
                messages.append(MessageItem(type="img", msg=m.url))
        elif isinstance(m, At):
            if group_id:
                if m.target == "0":
                    uname = "全体成员"
                else:
                    uname = m.target
                    if group_id not in ID2NAME:
                        ID2NAME[group_id] = {}
                    if m.target in ID2NAME[group_id]:
                        uname = ID2NAME[group_id][m.target]
                    elif group_user := await GroupInfoUser.get_or_none(
                        user_id=m.target, group_id=group_id
                    ):
                        uname = group_user.user_name
                        if m.target not in ID2NAME[group_id]:
                            ID2NAME[group_id][m.target] = uname
                messages.append(MessageItem(type="at", msg=f"@{uname}"))
        elif isinstance(m, Hyper):
            messages.append(MessageItem(type="text", msg="[分享消息]"))
    return messages


@matcher.handle()
async def _(
    message: UniMsg, event: MessageEvent, session: EventSession, uname: str = UserName()
):
    global ws_conn, ID2NAME, ID_LIST
    uid = session.id1
    if ws_conn and ws_conn.client_state == WebSocketState.CONNECTED and uid:
        msg_id = event.message_id
        if msg_id in ID_LIST:
            return
        ID_LIST.append(msg_id)
        if len(ID_LIST) > 50:
            ID_LIST = ID_LIST[40:]
        gid = session.id3 or session.id2
        messages = await message_handle(message, gid)
        data = Message(
            object_id=gid or uid,
            user_id=uid,
            group_id=gid,
            message=messages,
            name=uname,
            ava_url=AVA_URL.format(uid),
        )
        await ws_conn.send_json(data.dict())
