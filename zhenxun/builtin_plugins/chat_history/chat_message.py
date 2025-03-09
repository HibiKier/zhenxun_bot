import nonebot
from nonebot import on_message
from nonebot.drivers import Driver
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.models.chat_history import ChatHistory
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

__plugin_meta__ = PluginMetadata(
    name="消息存储",
    description="消息存储，被动存储群消息",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
        configs=[
            RegisterConfig(
                module="chat_history",
                key="FLAG",
                value=True,
                help="是否开启消息自从存储",
                default_value=True,
                type=bool,
            )
        ],
    ).to_dict(),
)

from .message_maneger import MessageProcessor

driver: Driver = nonebot.get_driver()
MeaasgeQueue: MessageProcessor | None = None


@driver.on_bot_connect
async def init_queue():
    """启动时初始化消息队列"""
    try:
        global MessageQueue
        MessageQueue = MessageProcessor()
        await MessageQueue.start()
        logger.info("消息队列初始化成功", "QueueInit", adapter="ChatHistory")
    except Exception as e:
        logger.error("消息队列初始化失败", "QueueInit", adapter="ChatHistory", e=e)


@driver.on_bot_disconnect
async def shutdown_queue():
    """关闭时停止消息队列"""
    try:
        global MessageQueue
        if MessageQueue is not None:
            await MessageQueue.stop()
            logger.info("消息队列已停止", "QueueShutdown", adapter="ChatHistory")
    except Exception as e:
        logger.error("消息队列停止失败", "QueueShutdown", adapter="ChatHistory", e=e)


def rule(message: UniMsg) -> bool:
    """消息处理规则"""
    return bool(Config.get_config("chat_history", "FLAG") and message)


chat_history = on_message(rule=rule, priority=1, block=False)


@chat_history.handle()
async def _(message: UniMsg, session: Uninfo):
    """处理消息存储"""
    try:
        global MessageQueue
        if MessageQueue is None:
            logger.warning("消息队列未初始化", "MessageQueue", session=session)
            return

        history = ChatHistory(
            user_id=session.user.id,
            group_id=session.scene.id,
            text=str(message),
            plain_text=message.extract_plain_text(),
            bot_id=session.self_id,
            platform=session.scope,
        )

        if not await MessageQueue.add_message(history):
            logger.warning("消息入队失败", "MessageQueue", session=session)

        logger.debug("消息入队成功", "MessageQueue", session=session)

    except Exception as e:
        logger.error("消息处理失败", "MessageQueue", session=session, e=e)
