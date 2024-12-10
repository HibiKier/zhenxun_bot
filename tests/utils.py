import json
from pathlib import Path

from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.adapters.onebot.v11.event import Sender


def get_response_json(base_path: Path, file: str) -> dict:
    try:
        return json.loads(
            (Path(__file__).parent / "response" / base_path / file).read_text(
                encoding="utf8"
            )
        )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error reading or parsing JSON file: {e}") from e


def get_content_bytes(base_path: Path, path: str) -> bytes:
    try:
        return (Path(__file__).parent / "content" / base_path / path).read_bytes()
    except FileNotFoundError as e:
        raise ValueError(f"Error reading file: {e}") from e


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
