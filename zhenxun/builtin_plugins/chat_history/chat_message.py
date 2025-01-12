import nonebot
from nonebot import on_message
from nonebot.drivers import Driver
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_uninfo import Uninfo

from zhenxun.configs.config import Config
from zhenxun.configs.utils import PluginExtraData, RegisterConfig
from zhenxun.models.chat_history import ChatHistory
from zhenxun.services.log import logger
from zhenxun.utils.enum import PluginType

from .data_source import AdaptiveMessageQueue, HealthCheckConfig

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

driver: Driver = nonebot.get_driver()


class MessageQueueManager:
    _instance: AdaptiveMessageQueue | None = None

    @classmethod
    def get_instance(cls) -> AdaptiveMessageQueue:
        if cls._instance is None:
            cls._instance = AdaptiveMessageQueue(
                initial_batch_size=1000,
                initial_flush_interval=60.0,
                max_retry=3,
                max_queue_size=50000,
                health_check_config=HealthCheckConfig(
                    max_delay_seconds=120.0,
                    max_queue_size=40000,
                    max_failure_rate=0.1,
                    max_retry_count=100,
                    max_load=0.9,
                ),
            )
        return cls._instance


@driver.on_startup
async def init_queue():
    """启动时初始化消息队列"""
    try:
        queue = MessageQueueManager.get_instance()
        await queue.start()
        logger.info("消息队列初始化成功", "QueueInit", adapter="ChatHistory")
    except Exception as e:
        logger.error("消息队列初始化失败", "QueueInit", adapter="ChatHistory", e=e)


@driver.on_shutdown
async def shutdown_queue():
    """关闭时停止消息队列"""
    try:
        if queue := MessageQueueManager.get_instance():
            await queue.stop()
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
        queue = MessageQueueManager.get_instance()
        history = ChatHistory(
            user_id=session.user.id,
            group_id=session.scene.id,
            text=str(message),
            plain_text=message.extract_plain_text(),
            bot_id=session.self_id,
            platform=session.platform,
        )

        if not await queue.put(history):
            logger.warning("消息入队失败", "MessageQueue", session=session)

    except Exception as e:
        logger.error("消息处理失败", "MessageQueue", session=session, e=e)


@scheduler.scheduled_job("interval", minutes=5)
async def check_queue_health():
    """定期检查队列健康状态"""
    try:
        queue = MessageQueueManager.get_instance()
        status = await queue.get_queue_status()

        if not status.is_healthy:
            info = (
                f"队列状态异常 - 大小: {status.queue_size}, "
                f"失败率: {status.metrics.failure_rate:.2%}, "
                f"消息率: {status.adaptive_metrics.current_message_rate:.1f}/min, "
                f"负载: {status.adaptive_metrics.current_load:.2f}"
            )
            logger.warning(info, "QueueHealth", adapter="ChatHistory")
    except Exception as e:
        logger.error("队列健康检查失败", "QueueHealth", adapter="ChatHistory", e=e)
