import json
from pathlib import Path

from nonebot.adapters.onebot.v11.event import Sender
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent


def get_response_json(path: str) -> dict:
    return json.loads(
        (Path(__file__).parent / "response" / path).read_text(encoding="utf8")
    )


def get_content_bytes(path: str) -> bytes:
    return (Path(__file__).parent / "content" / path).read_bytes()


def _v11_group_message_event(
    message: str,
    self_id: int,
    user_id: int,
    group_id: int,
    message_id: int,
    to_me: bool = True,
) -> GroupMessageEvent:
    return GroupMessageEvent(
        time=1122,
        self_id=self_id,
        post_type="message",
        sub_type="",
        user_id=user_id,
        message_id=message_id,
        message=Message(message),
        original_message=Message(message),
        message_type="group",
        raw_message=message,
        font=1,
        sender=Sender(user_id=user_id),
        to_me=to_me,
        group_id=group_id,
    )


def _v11_private_message_send(
    message: str,
    user_id: int,
):
    return {
        "message_type": "private",
        "user_id": user_id,
        "message": [
            MessageSegment(
                type="text",
                data={
                    "text": message,
                },
            )
        ],
    }
