import asyncio
from collections import deque
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo

from nonebot import on_message
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_session import EventSession
from tortoise import transactions

from zhenxun.configs.config import BotConfig, Config
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


def rule(message: UniMsg) -> bool:
    return bool(Config.get_config("chat_history", "FLAG") and message)


chat_history = on_message(rule=rule, priority=1, block=False)


@dataclass
class MessageQueueMetrics:
    """消息队列指标"""

    pending_count: int = 0
    processed_count: int = 0
    failed_count: int = 0
    retry_count: int = 0
    last_process_time: datetime | None = None
    avg_process_time: float = 0.0
    batch_size: int = 0
    messages_per_minute: float = 0.0
    _message_times: deque[datetime] = field(default_factory=lambda: deque(maxlen=10000))

    @property
    def total_processed(self) -> int:
        """总处理消息数（包括成功和失败）"""
        return self.processed_count + self.failed_count

    @property
    def failure_rate(self) -> float:
        """失败率"""
        if self.total_processed == 0:
            return 0.0
        return self.failed_count / self.total_processed

    def update_message_rate(self, current_time: datetime) -> None:
        """更新每分钟消息率"""
        while (
            self._message_times
            and (current_time - self._message_times[0]).total_seconds() > 60
        ):
            self._message_times.popleft()

        self.messages_per_minute = len(self._message_times)

    def add_message_timestamp(self, timestamp: datetime) -> None:
        """添加新消息的时间戳"""
        self._message_times.append(timestamp)

    def update_queue_size(self, size: int) -> None:
        """更新队列大小"""
        self.pending_count = size

    def clone(self) -> "MessageQueueMetrics":
        """克隆当前指标"""
        new_metrics = MessageQueueMetrics(
            pending_count=self.pending_count,
            retry_count=self.retry_count,
            processed_count=self.processed_count,
            failed_count=self.failed_count,
            last_process_time=self.last_process_time,
            avg_process_time=self.avg_process_time,
            batch_size=self.batch_size,
            messages_per_minute=self.messages_per_minute,
        )
        for timestamp in self._message_times:
            new_metrics.add_message_timestamp(timestamp)
        return new_metrics


class AsyncMessageQueue:
    def __init__(
        self, batch_size: int = 1000, flush_interval: float = 60.0, max_retry: int = 3
    ):
        """
        初始化消息队列

        Args:
            batch_size (int, optional): 批处理大小. Defaults to 1000.
            flush_interval (float, optional): 刷新间隔. Defaults to 60.0.
            max_retry (int, optional): 最大重试次数. Defaults to 3.
        """
        self._queue = asyncio.Queue()
        self._batch_size = batch_size
        self._flush_interval = flush_interval
        self._max_retry = max_retry
        self._metrics = MessageQueueMetrics(batch_size=batch_size)
        self._last_rate_update = datetime.now(ZoneInfo(BotConfig.time_zone))
        self._rate_update_interval = 1.0
        self._flush_task: asyncio.Task | None = None
        self._running = False
        self._processing_lock = asyncio.Lock()
        self._last_process_time: datetime | None = None

    async def start(self):
        """启动消息队列处理"""
        if not self._running:
            self._running = True
            self._flush_task = asyncio.create_task(self._auto_flush())
            logger.info("Message queue processor started")

    async def stop(self):
        """停止消息队列处理"""
        if self._running:
            self._running = False
            if self._flush_task:
                try:
                    await self._process_remaining()
                    await self._flush_task
                finally:
                    self._flush_task = None
                    logger.info("Message queue processor stopped")

    async def put(self, message: ChatHistory) -> bool:
        """添加消息到队列"""
        try:
            await self._queue.put(message)
            self._metrics.pending_count = self._queue.qsize()

            current_time = datetime.now(ZoneInfo(BotConfig.time_zone))
            self._metrics.add_message_timestamp(current_time)

            if (
                current_time - self._last_rate_update
            ).total_seconds() >= self._rate_update_interval:
                self._metrics.update_message_rate(current_time)
                self._last_rate_update = current_time

            return True
        except Exception as e:
            logger.error(f"Failed to queue message: {e}")
            return False

    @asynccontextmanager
    async def batch_get(self) -> AsyncIterator[list[ChatHistory]]:
        """获取一批消息的上下文管理器"""
        messages = []
        try:
            while len(messages) < self._batch_size and not self._queue.empty():
                try:
                    message = self._queue.get_nowait()
                    messages.append(message)
                except asyncio.QueueEmpty:
                    break
            yield messages
        finally:
            self._metrics.pending_count = self._queue.qsize()

    async def _auto_flush(self):
        """自动刷新队列，适应SQLite的特性"""
        while self._running:
            try:
                current_time = datetime.now(ZoneInfo(BotConfig.time_zone))

                if (
                    self._last_process_time is None
                    or (current_time - self._last_process_time).total_seconds()
                    >= self._flush_interval
                ):
                    await self._process_batch()

                await asyncio.sleep(min(10.0, self._flush_interval))

            except Exception as e:
                logger.error(f"Error in auto flush: {e}")
                await asyncio.sleep(1)

    async def _process_batch(self):
        """SQLite友好的批处理实现"""
        async with self._processing_lock:
            start_time = datetime.now(ZoneInfo(BotConfig.time_zone))
            async with self.batch_get() as messages:
                if not messages:
                    return

                try:
                    async with transactions.in_transaction():
                        await ChatHistory.bulk_create(messages)

                    process_time = (
                        datetime.now(ZoneInfo(BotConfig.time_zone)) - start_time
                    ).total_seconds()
                    self._update_metrics(len(messages), process_time)
                    self._last_process_time = datetime.now(
                        ZoneInfo(BotConfig.time_zone)
                    )
                    logger.debug(f"Successfully processed {len(messages)} messages")

                except Exception as e:
                    logger.error(f"Failed to process batch: {e}")
                    self._metrics.failed_count += len(messages)
                    await self._handle_failed_messages(messages, e)

    async def _handle_failed_messages(
        self, messages: list[ChatHistory], error: Exception
    ):
        """处理失败消息的逻辑"""
        # 记录失败的消息
        logger.error(
            f"Failed to process {len(messages)} messages. Error: {error!s}\n"
            f"First message: {messages[0] if messages else 'No messages'}"
        )

        for retry in range(self._max_retry):
            try:
                await asyncio.sleep(1 * (retry + 1))
                async with transactions.in_transaction():
                    await ChatHistory.bulk_create(messages)
                logger.info(f"Successfully processed messages after retry {retry + 1}")
                return
            except Exception as retry_error:
                logger.error(f"Retry {retry + 1} failed: {retry_error}")

            # 所有重试都失败后的处理
        logger.error(
            f"All retries failed for {len(messages)} messages. "
            "Consider implementing a dead letter queue."
        )

    async def _process_remaining(self):
        """处理队列中剩余的所有消息"""
        while not self._queue.empty():
            await self._process_batch()

    @property
    def queue_size(self) -> int:
        """当前队列大小"""
        return self._queue.qsize()

    async def get_queue_status(self) -> dict:
        """获取队列状态"""
        current_metrics = self.metrics
        return {
            "queue_size": self.queue_size,
            "last_process_time": self._last_process_time,
            "metrics": current_metrics.__dict__,
            "is_running": self._running,
            "is_healthy": self.is_healthy,
        }

    def _update_metrics(self, processed_count: int, process_time: float):
        """更新性能指标"""
        current_time = datetime.now(ZoneInfo(BotConfig.time_zone))
        self._metrics.last_process_time = current_time
        self._metrics.processed_count += processed_count
        if processed_count > 0:
            self._metrics.avg_process_time = (
                self._metrics.avg_process_time
                * (self._metrics.processed_count - processed_count)
                + process_time * processed_count
            ) / self._metrics.processed_count
        self._metrics.update_message_rate(current_time)

    async def get_detailed_metrics(self) -> MessageQueueMetrics:
        """获取详细的指标信息"""
        return self.metrics

    @property
    def metrics(self) -> MessageQueueMetrics:
        """获取当前指标"""
        self._metrics.update_queue_size(self._queue.qsize())
        self._metrics.update_message_rate(datetime.now(ZoneInfo(BotConfig.time_zone)))
        return self._metrics

    async def get_metrics_snapshot(self) -> MessageQueueMetrics:
        """获取指标的快照"""
        return self._metrics.clone()

    @property
    def is_healthy(self) -> bool:
        """检查队列健康状态"""
        metrics = self.metrics

        if not self._running:
            return False

        if metrics.last_process_time:
            delay = (
                datetime.now(ZoneInfo(BotConfig.time_zone)) - metrics.last_process_time
            ).total_seconds()
            if delay > self._flush_interval * 2:
                return False
        return metrics.total_processed <= 0 or metrics.failure_rate <= 0.1


TEMP_LIST = []


@chat_history.handle()
async def _(message: UniMsg, session: EventSession):
    # group_id = session.id3 or session.id2
    group_id = session.id2
    TEMP_LIST.append(
        ChatHistory(
            user_id=session.id1,
            group_id=group_id,
            text=str(message),
            plain_text=message.extract_plain_text(),
            bot_id=session.bot_id,
            platform=session.platform,
        )
    )


@scheduler.scheduled_job(
    "interval",
    minutes=1,
)
async def _():
    try:
        message_list = TEMP_LIST.copy()
        TEMP_LIST.clear()
        if message_list:
            await ChatHistory.bulk_create(message_list)
        logger.debug(f"批量添加聊天记录 {len(message_list)} 条", "定时任务")
    except Exception as e:
        logger.error("定时批量添加聊天记录", "定时任务", e=e)
