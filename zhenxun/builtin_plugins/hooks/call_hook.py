from typing import Any

from nonebot.adapters import Bot

from zhenxun.services.log import logger
from zhenxun.utils.manager.message_manager import MessageManager


@Bot.on_called_api
async def handle_api_result(
    bot: Bot, exception: Exception | None, api: str, data: dict[str, Any], result: Any
):
    if not exception and api == "send_msg":
        try:
            if (uid := data.get("user_id")) and (msg_id := result.get("message_id")):
                MessageManager.add(str(uid), str(msg_id))
                logger.debug(
                    f"收集消息id，user_id: {uid}, msg_id: {msg_id}", "msg_hook"
                )
        except Exception as e:
            logger.warning(
                f"收集消息id发生错误...data: {data}, result: {result}", "msg_hook", e=e
            )
