import asyncio
from collections import deque
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import NamedTuple
from zoneinfo import ZoneInfo

from tortoise import transactions

from zhenxun.configs.config import BotConfig
from zhenxun.models.chat_history import ChatHistory
from zhenxun.services.log import logger


@dataclass
class MessageQueueMetrics:
    """消息队列指标"""

    pending_count: int = 0
    """等待处理的消息数量"""
    processed_count: int = 0
    """已处理的消息数量"""
    failed_count: int = 0
    """处理失败的消息数量"""
    retry_count: int = 0
    """消息重试次数"""
    last_process_time: datetime | None = None
    """上一次处理消息的时间"""
    avg_process_time: float = 0.0
    """平均处理时间（单位：秒）"""
    batch_size: int = 0
    """每次批处理的消息数量"""
    messages_per_minute: float = 0.0
    """每分钟处理的消息数量"""
    _message_times: deque[datetime] = field(default_factory=lambda: deque(maxlen=10000))
    """消息的时间戳队列，用于计算消息速率"""

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
        """克隆当前消息队列指标"""
        return deepcopy(self)


@dataclass
class HealthCheckConfig:
    """健康检查配置"""

    max_delay_seconds: float = 60.0
    """最大处理延迟时间（单位：秒）"""
    max_queue_size: int = 10000
    """队列允许的最大消息数量"""
    max_failure_rate: float = 0.1
    """允许的最大失败率"""
    max_retry_count: int = 100
    """允许的最大重试次数"""
    max_load: float = 0.9
    """允许的最大负载"""


@dataclass
class AdaptiveMetrics:
    """自适应指标"""

    current_message_rate: float
    """当前消息处理速率（每分钟消息数）"""
    current_load: float
    """当前负载（比例值）"""
    average_load_1m: float
    """过去 1 分钟的平均负载"""
    average_load_5m: float
    """过去 5 分钟的平均负载"""
    batch_size: int
    """当前批处理的大小"""
    flush_interval: float
    """当前刷新间隔（单位：秒）"""
    last_adjustment: datetime
    """最后一次调整时间"""
    load_statistics: dict
    """负载统计信息"""


@dataclass
class QueueConfiguration:
    """队列配置"""

    batch_size: int
    """每批次处理的消息数量"""
    flush_interval: float
    """刷新间隔（单位：秒）"""
    max_retry: int
    """最大重试次数"""
    min_batch_size: int
    """最小批处理大小"""
    max_batch_size: int
    """最大批处理大小"""
    min_flush_interval: float
    """最小刷新间隔（单位：秒）"""
    max_flush_interval: float
    """最大刷新间隔（单位：秒）"""
    load_check_interval: float
    """负载检查间隔（单位：秒）"""
    window_size: int
    """负载窗口大小（单位：秒）"""
    load_thresholds: dict
    """负载阈值配置"""


@dataclass
class QueueStatus:
    """队列状态数据类"""

    queue_size: int
    """当前队列大小"""
    last_process_time: datetime | None
    """上次处理消息的时间"""
    is_running: bool
    """队列是否正在运行"""
    is_healthy: bool
    """队列是否健康"""
    metrics: MessageQueueMetrics
    """消息队列指标"""
    adaptive_metrics: AdaptiveMetrics
    """自适应指标"""
    configuration: QueueConfiguration
    """队列配置"""

    @classmethod
    def create(
        cls,
        queue: "AdaptiveMessageQueue",
        metrics: MessageQueueMetrics,
        adaptive_metrics: AdaptiveMetrics,
        configuration: QueueConfiguration,
    ) -> "QueueStatus":
        """创建队列状态实例"""
        return cls(
            queue_size=queue.queue_size,
            last_process_time=queue.last_process_time,
            is_running=queue.running,
            is_healthy=queue.is_healthy,
            metrics=metrics,
            adaptive_metrics=adaptive_metrics,
            configuration=configuration,
        )


class QueueAdjustmentConfig(NamedTuple):
    """队列调整配置"""

    min_batch_size: int = 100
    """最小批处理大小"""
    max_batch_size: int = 5000
    """最大批处理大小"""
    min_flush_interval: float = 30.0
    """最小刷新间隔（单位：秒）"""
    max_flush_interval: float = 300.0  # 5分钟
    """最大刷新间隔（单位：秒）"""
    load_check_interval: float = 30.0  # 负载检查间隔
    """负载检查间隔（单位：秒）"""
    window_size: int = 300  # 5分钟窗口大小
    """负载统计窗口大小（单位：秒）"""


@dataclass
class QueueLoadMetrics:
    """队列负载指标"""

    window_size: int = 300  # 5分钟窗口
    """负载统计窗口大小（单位：秒）"""
    low_threshold: float = 100  # 每分钟消息数的低阈值
    """每分钟消息数的低阈值"""
    high_threshold: float = 1000  # 每分钟消息数的高阈值
    """每分钟消息数的高阈值"""
    current_load: float = 0.0
    """当前负载"""
    last_adjustment: datetime = field(
        default_factory=lambda: datetime.now(ZoneInfo(BotConfig.time_zone))
    )
    """最后一次调整时间"""
    load_history: deque[tuple[datetime, float]] = field(
        default_factory=lambda: deque(maxlen=1000)
    )
    """负载历史记录"""

    def add_load_sample(self, load: float):
        """添加负载采样"""
        current_time = datetime.now(ZoneInfo(BotConfig.time_zone))
        self.load_history.append((current_time, load))

        # 清理超过窗口的历史数据
        while (
            self.load_history
            and (current_time - self.load_history[0][0]).total_seconds()
            > self.window_size
        ):
            self.load_history.popleft()

    def get_average_load(self, window_seconds: int | None = None) -> float:
        """获取指定时间窗口的平均负载"""
        if not self.load_history:
            return 0.0

        current_time = datetime.now(ZoneInfo(BotConfig.time_zone))
        window = window_seconds if window_seconds is not None else self.window_size

        # 筛选时间窗口内的负载数据
        recent_loads = [
            load
            for time, load in self.load_history
            if (current_time - time).total_seconds() <= window
        ]

        return sum(recent_loads) / len(recent_loads) if recent_loads else 0.0

    def get_load_statistics(self) -> dict:
        """获取负载统计信息"""
        if not self.load_history:
            return {
                "min_load": 0.0,
                "max_load": 0.0,
                "avg_load": 0.0,
                "samples_count": 0,
            }

        loads = [load for _, load in self.load_history]
        return {
            "min_load": min(loads),
            "max_load": max(loads),
            "avg_load": sum(loads) / len(loads),
            "samples_count": len(loads),
        }

    def clear_old_history(self, max_age: int | None = None):
        """清理旧的负载历史数据"""
        if max_age is None:
            max_age = self.window_size * 2

        current_time = datetime.now(ZoneInfo(BotConfig.time_zone))
        while (
            self.load_history
            and (current_time - self.load_history[0][0]).total_seconds() > max_age
        ):
            self.load_history.popleft()


class AdaptiveMessageQueue:
    def __init__(
        self,
        initial_batch_size: int = 1000,
        initial_flush_interval: float = 60.0,
        max_retry: int = 3,
        config: QueueAdjustmentConfig | None = None,
        max_queue_size: int = 50000,
        health_check_config: HealthCheckConfig | None = None,
    ):
        """
        初始化自适应消息队列

        Args:
            initial_batch_size (int): 初始批处理大小
            initial_flush_interval (float): 初始刷新间隔
            max_retry (int): 最大重试次数
            config (QueueAdjustmentConfig, optional): 队列调整配置
        """
        if initial_batch_size <= 0:
            raise ValueError("initial_batch_size must be positive")
        if initial_flush_interval <= 0:
            raise ValueError("initial_flush_interval must be positive")
        if max_retry < 0:
            raise ValueError("max_retry must be non-negative")
        self._queue = asyncio.Queue(maxsize=max_queue_size)
        self._batch_size = initial_batch_size
        self._flush_interval = initial_flush_interval
        self._max_retry = max_retry
        self._metrics = MessageQueueMetrics(batch_size=initial_batch_size)
        self._config = config or QueueAdjustmentConfig()
        self._load_metrics = QueueLoadMetrics(window_size=self._config.window_size)

        self._last_rate_update = datetime.now(ZoneInfo(BotConfig.time_zone))
        self._rate_update_interval = 1.0
        self._flush_task: asyncio.Task | None = None
        self._adjustment_task: asyncio.Task | None = None
        self._running = False
        self._processing_lock = asyncio.Lock()
        self._last_process_time: datetime | None = None

        self._health_config = health_check_config or HealthCheckConfig()
        self._last_empty_check = datetime.now(ZoneInfo(BotConfig.time_zone))
        self._idle_check_interval = 60.0
        self._immediate_process_tasks: set[asyncio.Task] = set()

    async def start(self) -> None:
        """启动消息队列处理和动态调整"""
        if not self._running:
            self._running = True
            self._flush_task = asyncio.create_task(self._auto_flush())
            self._adjustment_task = asyncio.create_task(
                self._auto_adjust_queue_params()
            )
            logger.info(
                "Adaptive message queue processor started with "
                f"batch_size={self._batch_size}, flush_interval={self._flush_interval}"
            )

    async def stop(self) -> None:
        """停止消息队列处理和动态调整"""
        if not self._running:
            return
        self._running = False

        for task in self._immediate_process_tasks:
            task.cancel()

        await asyncio.gather(*self._immediate_process_tasks, return_exceptions=True)
        self._immediate_process_tasks.clear()

        if self._adjustment_task:
            self._adjustment_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._adjustment_task
            self._adjustment_task = None

        if self._flush_task:
            try:
                await self._process_remaining()
                await self._flush_task
            except asyncio.CancelledError:
                pass
            finally:
                self._flush_task = None
                logger.info("Adaptive message queue processor stopped")

    async def put(self, message: ChatHistory) -> bool:
        """添加消息到队列"""
        try:
            # 如果队列已满，等待一个短暂的时间
            try:
                await asyncio.wait_for(self._queue.put(message), timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Queue is full, message dropped")
                return False

            self._metrics.pending_count = self._queue.qsize()
            current_time = datetime.now(ZoneInfo(BotConfig.time_zone))
            self._metrics.add_message_timestamp(current_time)

            if (
                current_time - self._last_rate_update
            ).total_seconds() >= self._rate_update_interval:
                self._metrics.update_message_rate(current_time)
                self._last_rate_update = current_time

            # 如果队列大小达到批处理大小，立即触发处理
            if self._queue.qsize() >= self._batch_size:
                task = asyncio.create_task(self._trigger_immediate_process())
                self._immediate_process_tasks.add(task)
                task.add_done_callback(self._immediate_process_tasks.discard)

            return True
        except Exception as e:
            logger.error(f"Failed to queue message: {e}")
            return False

    async def _trigger_immediate_process(self) -> None:
        """触发即时批处理"""
        if not self._processing_lock.locked():
            try:
                async with self._processing_lock:
                    await self._process_batch()
            except Exception as e:
                logger.error(f"Error in immediate batch processing: {e}")

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

    def _calculate_message_rate(self) -> float:
        """计算当前5分钟内的每分钟消息率"""
        current_time = datetime.now(ZoneInfo(BotConfig.time_zone))
        window_start = current_time - timedelta(seconds=self._load_metrics.window_size)

        # 清理超出时间窗口的消息时间戳
        while (
            self._metrics._message_times
            and self._metrics._message_times[0] < window_start
        ):
            self._metrics._message_times.popleft()

        # 计算5分钟内的平均每分钟消息数
        messages_in_window = len(self._metrics._message_times)
        minutes_in_window = (
            min(
                self._load_metrics.window_size / 60,
                (
                    current_time
                    - (
                        self._metrics._message_times[0]
                        if self._metrics._message_times
                        else current_time
                    )
                ).total_seconds()
                / 60,
            )
            or 1
        )

        return messages_in_window / minutes_in_window

    def _adjust_queue_parameters(self, message_rate: float) -> tuple[int, float]:
        """根据消息率调整队列参数"""
        current_time = datetime.now(ZoneInfo(BotConfig.time_zone))

        # 如果距离上次调整时间太短，直接返回当前值
        if (
            current_time - self._load_metrics.last_adjustment
        ).total_seconds() < self._config.load_check_interval:
            return self._batch_size, self._flush_interval

        # 计算负载水平 (0-1之间的值)
        load_level = (message_rate - self._load_metrics.low_threshold) / (
            self._load_metrics.high_threshold - self._load_metrics.low_threshold
        )
        load_level = max(0.0, min(1.0, load_level))

        # 添加负载采样
        self._load_metrics.add_load_sample(load_level)

        # 使用平均负载来平滑调整
        avg_load = self._load_metrics.get_average_load(60)  # 使用1分钟平均负载

        # 动态调整批处理大小
        new_batch_size = int(
            self._config.min_batch_size
            + (self._config.max_batch_size - self._config.min_batch_size) * avg_load
        )

        # 动态调整刷新间隔
        new_flush_interval = (
            self._config.min_flush_interval
            + (self._config.max_flush_interval - self._config.min_flush_interval)
            * avg_load
        )

        # 记录调整时间和当前负载
        self._load_metrics.last_adjustment = current_time
        self._load_metrics.current_load = avg_load

        return new_batch_size, new_flush_interval

    async def _auto_adjust_queue_params(self) -> None:
        """自动调整队列参数的后台任务"""
        while self._running:
            try:
                message_rate = self._calculate_message_rate()

                # 调整队列参数
                new_batch_size, new_flush_interval = self._adjust_queue_parameters(
                    message_rate
                )

                # 应用新的参数
                if (
                    new_batch_size != self._batch_size
                    or new_flush_interval != self._flush_interval
                ):
                    old_batch_size, old_flush_interval = (
                        self._batch_size,
                        self._flush_interval,
                    )
                    self._batch_size = new_batch_size
                    self._flush_interval = new_flush_interval
                    logger.info(
                        f"Queue parameters adjusted: "
                        f"batch_size: {old_batch_size}->{new_batch_size}, "
                        f"flush_interval: {old_flush_interval:.1f}->"
                        f"{new_flush_interval:.1f}s "
                        f"(message rate: {message_rate:.1f}/min, "
                        f"load: {self._load_metrics.current_load:.2f})"
                    )

                await asyncio.sleep(self._config.load_check_interval)
            except Exception as e:
                logger.error(f"Error in queue parameter adjustment: {e}")
                await asyncio.sleep(5)

    async def _auto_flush(self) -> None:
        """自动刷新队列"""
        while self._running:
            try:
                current_time = datetime.now(ZoneInfo(BotConfig.time_zone))

                # 检查是否需要处理
                should_process = (
                    self._last_process_time is None
                    or (current_time - self._last_process_time).total_seconds()
                    >= self._flush_interval
                )

                if should_process:
                    await self._process_batch()

                if self._queue.empty():
                    if (
                        current_time - self._last_empty_check
                    ).total_seconds() >= self._idle_check_interval:
                        await asyncio.sleep(
                            min(self._flush_interval * 2, self._idle_check_interval)
                        )
                        self._last_empty_check = current_time
                        continue
                else:
                    self._last_empty_check = current_time

                await asyncio.sleep(min(10.0, self._flush_interval))

            except Exception as e:
                logger.error(f"Error in auto flush: {e}")
                await asyncio.sleep(1)

    async def _process_batch(self) -> None:
        """处理一批消息"""
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
        logger.error(f"Failed to process {len(messages)} messages. Error: {error!s}")

        # 将消息分组进行重试
        chunk_size = min(100, len(messages))  # 较小的批次重试
        for i in range(0, len(messages), chunk_size):
            chunk = messages[i : i + chunk_size]

            for retry in range(self._max_retry):
                try:
                    await asyncio.sleep(1 * (retry + 1))
                    async with transactions.in_transaction():
                        for msg in chunk:
                            try:
                                await ChatHistory.create(**msg.__dict__)
                            except Exception as e:
                                logger.error(f"Failed to insert message: {e}")
                                self._metrics.failed_count += 1
                                continue

                    logger.info(
                        f"Successfully processed chunk {i // chunk_size + 1} "
                        f"after retry {retry + 1}"
                    )
                    break
                except Exception as retry_error:
                    logger.error(
                        f"Retry {retry + 1} failed for chunk "
                        f"{i // chunk_size + 1}: {retry_error}"
                    )
                    self._metrics.retry_count += 1
                    if retry == self._max_retry - 1:
                        logger.error(
                            f"All retries failed for chunk {i // chunk_size + 1}"
                        )

    async def _process_remaining(self):
        """处理队列中剩余的所有消息"""
        while not self._queue.empty():
            await self._process_batch()

    @property
    def queue_size(self) -> int:
        """当前队列大小"""
        return self._queue.qsize()

    async def get_queue_status(self) -> QueueStatus:
        """获取队列状态"""
        current_metrics = self.metrics

        adaptive_metrics = AdaptiveMetrics(
            current_message_rate=self._calculate_message_rate(),
            current_load=self._load_metrics.current_load,
            average_load_1m=self._load_metrics.get_average_load(60),
            average_load_5m=self._load_metrics.get_average_load(300),
            batch_size=self._batch_size,
            flush_interval=self._flush_interval,
            last_adjustment=self._load_metrics.last_adjustment,
            load_statistics=self._load_metrics.get_load_statistics(),
        )

        configuration = QueueConfiguration(
            batch_size=self._batch_size,
            flush_interval=self._flush_interval,
            max_retry=self._max_retry,
            min_batch_size=self._config.min_batch_size,
            max_batch_size=self._config.max_batch_size,
            min_flush_interval=self._config.min_flush_interval,
            max_flush_interval=self._config.max_flush_interval,
            load_check_interval=self._config.load_check_interval,
            window_size=self._config.window_size,
            load_thresholds={
                "low": self._load_metrics.low_threshold,
                "high": self._load_metrics.high_threshold,
            },
        )

        return QueueStatus.create(
            queue=self,
            metrics=current_metrics,
            adaptive_metrics=adaptive_metrics,
            configuration=configuration,
        )

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

    @property
    def metrics(self) -> MessageQueueMetrics:
        """获取当前指标"""
        self._metrics.update_queue_size(self._queue.qsize())
        self._metrics.update_message_rate(datetime.now(ZoneInfo(BotConfig.time_zone)))
        return self._metrics

    @property
    def is_healthy(self) -> bool:
        """检查队列健康状态"""
        metrics = self.metrics
        current_time = datetime.now(ZoneInfo(BotConfig.time_zone))

        if not self._running:
            return False

        if metrics.last_process_time:
            delay = (current_time - metrics.last_process_time).total_seconds()
            if delay > self._health_config.max_delay_seconds:
                logger.warning(f"Queue processing delay: {delay:.1f}s")
                return False

        if self.queue_size > self._health_config.max_queue_size:
            logger.warning(f"Queue size too large: {self.queue_size}")
            return False

        if (
            metrics.total_processed > 0
            and metrics.failure_rate > self._health_config.max_failure_rate
        ):
            logger.warning(f"High failure rate: {metrics.failure_rate:.2%}")
            return False

        if metrics.retry_count > self._health_config.max_retry_count:
            logger.warning(f"Too many retries: {metrics.retry_count}")
            return False

        if self._load_metrics.current_load > self._health_config.max_load:
            logger.warning(f"High load: {self._load_metrics.current_load:.2f}")
            return False

        return True

    @property
    def last_process_time(self) -> datetime | None:
        return self._last_process_time

    @property
    def running(self) -> bool:
        return self._running
