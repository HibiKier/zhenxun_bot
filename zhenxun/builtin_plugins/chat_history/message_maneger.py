from collections import deque
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Generic, Protocol, TypeVar

from anyio import (
    ClosedResourceError,
    Event,
    create_memory_object_stream,
    create_task_group,
    move_on_after,
    sleep,
)
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from zhenxun.configs.config import BotConfig
from zhenxun.services.log import logger

from ...models.chat_history import ChatHistory
from .types import QueueConfig

T = TypeVar("T")
Entity = TypeVar("Entity")
Row = TypeVar("Row")


@dataclass
class QueueMetrics:
    """队列性能指标"""

    config: QueueConfig
    message_count: int = 0  # 总消息计数
    batch_count: int = 0  # 批处理计数
    retry_count: int = 0  # 重试计数
    error_count: int = 0  # 错误计数
    process_time: float = 0  # 总处理时间（秒）

    # 滑动窗口存储
    message_window: deque[datetime] = field(
        default_factory=lambda: deque(maxlen=1000)
    )  # 消息时间窗口
    process_times: deque[float] = field(
        default_factory=lambda: deque(maxlen=100)
    )  # 处理时间窗口
    load_samples: deque[float] = field(
        default_factory=lambda: deque(maxlen=10)
    )  # 负载样本窗口

    def get_queue_size(self) -> int:
        """获取当前队列大小"""
        return len(self.message_window)

    def add_message(self) -> None:
        """记录一条新消息"""
        self.message_count += 1
        self.message_window.append(datetime.now(tz=BotConfig.timezone))

    def add_batch(self, process_time: float) -> None:
        """记录一个批次处理"""
        self.batch_count += 1
        self.process_time += process_time
        self.process_times.append(process_time)

    def add_load_sample(self, load: float) -> None:
        """添加负载样本"""
        self.load_samples.append(load)

    def get_message_rate(self, window_seconds: int) -> float:
        """计算指定窗口的消息速率（条/分钟）"""
        if not self.message_window:
            return 0.0

        current_time = datetime.now(tz=BotConfig.timezone)
        window_start = current_time - timedelta(seconds=window_seconds)
        recent_messages = sum(t >= window_start for t in self.message_window)

        minutes = window_seconds / 60.0
        return recent_messages / minutes if minutes > 0 else 0

    def get_average_process_time(self) -> float:
        """获取平均处理时间（秒）"""
        if not self.process_times:
            return 0.1
        return sum(self.process_times) / len(self.process_times)

    def get_average_load(self) -> float:
        """计算平均负载水平（0-1）"""
        if not self.load_samples:
            return 0.5
        return sum(self.load_samples) / len(self.load_samples)


class AdaptiveTimeSlider:
    """自适应时间滑块，管理批处理延时和大小调整"""

    def __init__(self, config: QueueConfig, queue_manager: "QueueManager"):
        self.config = config
        self.metrics = QueueMetrics(config=config)
        self._queue_manager = queue_manager

        # 当前参数
        self._batch_size = config.batch_size
        self._flush_interval = config.flush_interval

        # 上次调整时间
        self._last_adjustment = datetime.now(tz=BotConfig.timezone)

        # 负载阈值
        self.low_threshold = config.load_thresholds["low"]
        self.high_threshold = config.load_thresholds["high"]

        self._last_queue_size = 0

    @property
    def batch_size(self) -> int:
        """获取当前批大小"""
        return self._batch_size

    @property
    def flush_interval(self) -> float:
        """获取当前刷新间隔"""
        return self._flush_interval

    def record_message(self):
        """记录消息到达"""
        self.metrics.add_message()

    def record_batch_process(self, process_time: float):
        """记录批处理执行情况"""
        self.metrics.add_batch(process_time)

    def should_adjust(self) -> bool:
        """检查是否应该调整参数"""
        current_time = datetime.now(tz=BotConfig.timezone)
        return (
            current_time - self._last_adjustment
        ).total_seconds() >= self.config.load_check_interval

    def adjust_parameters(self) -> tuple[int, float] | None:
        """调整批处理参数并返回新值，如果不需要调整则返回 None"""
        if not self.should_adjust():
            return None

        # 获取实际队列大小
        current_queue_size = self._queue_manager.get_queue_size()
        message_rate = self.metrics.get_message_rate(self.config.window_size)
        avg_process_time = self.metrics.get_average_process_time()

        # 计算队列增长情况
        queue_growth = current_queue_size - self._last_queue_size
        backlog_factor = min(1.0, current_queue_size / self.config.max_queue_size)

        # 计算目标批处理大小
        messages_per_second = message_rate / 60
        target_batch_size = max(
            self.config.min_batch_size,
            min(
                self.config.max_batch_size,
                int(max(messages_per_second * 5, current_queue_size * 0.2)),
                # 考虑消息速率和当前队列大小
            ),
        )

        if queue_growth > 0 or backlog_factor > 0.1:
            # 队列在增长或有积压时，更激进地增加批处理大小
            new_batch_size = min(
                self.config.max_batch_size,
                max(
                    self._batch_size + max(5, int(self._batch_size * 0.3)),
                    # 至少增加5，或增加30%
                    target_batch_size,
                ),
            )
            # 减小处理间隔
            new_flush_interval = max(
                self.config.min_flush_interval,
                min(
                    self._flush_interval * 0.8,  # 最多减少20%
                    max(avg_process_time * 2, 5.0),  # 不小于处理时间的2倍且不小于5秒
                ),
            )
        else:
            # 队列在减小时，缓慢调整
            decrease_rate = 0.1  # 每次最多减少10%
            if current_queue_size > 0:
                # 仍有待处理消息时保持相对较大的批处理大小
                new_batch_size = max(
                    target_batch_size, int(self._batch_size * (1 - decrease_rate))
                )
            else:
                # 队列为空时才考虑更小的批处理大小
                new_batch_size = max(
                    self.config.min_batch_size,
                    int(self._batch_size * (1 - decrease_rate)),
                )

            # 处理间隔缓慢恢复
            new_flush_interval = min(
                self.config.max_flush_interval,
                self._flush_interval * (1 + decrease_rate),
            )

        # 应用变化限制
        max_batch_change = max(
            int(self._batch_size * 0.3), 5
        )  # 每次最多变化30%，但至少5
        new_batch_size = max(
            self._batch_size - max_batch_change,
            min(self._batch_size + max_batch_change, new_batch_size),
        )

        # 确保批处理大小不会低于一个最小合理值
        min_reasonable_batch = max(
            self.config.min_batch_size,
            min(10, int(message_rate / 6)),  # 至少能处理10秒内的消息
        )
        new_batch_size = max(min_reasonable_batch, new_batch_size)

        # 确保参数在合理范围内
        new_batch_size = max(
            self.config.min_batch_size, min(self.config.max_batch_size, new_batch_size)
        )
        new_flush_interval = max(
            self.config.min_flush_interval,
            min(self.config.max_flush_interval, new_flush_interval),
        )

        # 只在参数变化显著时更新
        if (
            abs(new_batch_size - self._batch_size) < 2
            and abs(new_flush_interval - self._flush_interval) <= 0.5
            and backlog_factor <= 0.1
        ):
            return None

        # 更新参数
        old_batch_size, old_flush_interval = self._batch_size, self._flush_interval
        self._batch_size = int(new_batch_size)
        self._flush_interval = new_flush_interval
        self._last_adjustment = datetime.now(tz=BotConfig.timezone)
        self._last_queue_size = current_queue_size

        logger.info(
            f"队列参数已调整: batch_size={old_batch_size}->{self._batch_size}, "
            f"flush_interval={old_flush_interval:.1f}s->{self._flush_interval:.1f}s "
            f"(消息速率: {message_rate:.1f}/分钟, 队列大小: {current_queue_size}, "
            f"队列增长: {queue_growth:+d}, 目标批大小: {target_batch_size})"
        )

        return self._batch_size, self._flush_interval


class QueueManager(Generic[T]):
    def __init__(
        self,
        processor: Callable[[list[T]], Awaitable[None]],
        queue_config: QueueConfig = QueueConfig(),
    ):
        self.queue_config = queue_config
        self.processor = processor
        self._send_stream: MemoryObjectSendStream[T] | None = None
        self._receive_stream: MemoryObjectReceiveStream[T] | None = None
        self._running = False
        self.time_slider = AdaptiveTimeSlider(queue_config, self)
        self._task_group = None
        self._new_message_event = Event()
        self._batch: list[T] = []
        self._batch_start_time = datetime.now(tz=BotConfig.timezone)
        self._next_process_time: datetime | None = None
        self._force_process = False
        self._last_process_time = datetime.now(tz=BotConfig.timezone)
        self._processing_lock = False

    async def start(self) -> None:
        if self._running:
            return

        self._send_stream, self._receive_stream = create_memory_object_stream(
            max_buffer_size=self.queue_config.max_queue_size
        )
        self._running = True
        self._batch = []
        self._batch_start_time = datetime.now(tz=BotConfig.timezone)
        self._next_process_time = self._calculate_next_process_time()

        self._task_group = create_task_group()
        async with self._task_group:
            self._task_group.start_soon(self._schedule_processing)
            self._task_group.start_soon(self._parameter_adjustment_task)

    def _calculate_next_process_time(self) -> datetime:
        """计算下次处理时间"""
        current_time = datetime.now(tz=BotConfig.timezone)
        return current_time + timedelta(seconds=self.time_slider.flush_interval)

    async def _schedule_processing(self):
        """调度队列处理"""
        if self._receive_stream is None:
            return

        while self._running:
            try:
                current_time = datetime.now(tz=BotConfig.timezone)

                # 初始化下次处理时间
                if self._next_process_time is None:
                    self._next_process_time = self._calculate_next_process_time()

                # 检查是否需要处理
                should_process = (
                    len(self._batch) >= self.time_slider.batch_size  # 批次已满
                    or (  # 或者到达处理时间且有消息待处理
                        current_time >= self._next_process_time
                        and (
                            len(self._batch) > 0
                            or self._receive_stream.statistics().current_buffer_used > 0
                        )
                    )
                    or self._force_process  # 或者被强制处理
                )

                if should_process and not self._processing_lock:
                    self._processing_lock = True
                    try:
                        await self._process_queue_step()
                        self._last_process_time = current_time
                        self._next_process_time = self._calculate_next_process_time()
                    finally:
                        self._processing_lock = False
                        self._force_process = False
                        self._new_message_event = Event()

                # 等待新消息或下次处理时间
                time_until_next = (
                    self._next_process_time - current_time
                ).total_seconds()

                if time_until_next > 0:
                    with move_on_after(min(time_until_next, 1.0)):
                        await self._new_message_event.wait()

                # 检查是否太久没有处理消息
                if (
                    len(self._batch) > 0
                    and (current_time - self._last_process_time).total_seconds()
                    > self.time_slider.flush_interval * 2
                ):
                    logger.warning(
                        f"队列处理延迟过长: {len(self._batch)} 条消息待处理, "
                    )
                    self._force_process = True

                await sleep(0.01)

            except Exception as e:
                logger.error(f"队列调度发生错误: {e}")
                await sleep(1)

    async def _process_queue_step(self):
        """处理队列的一个步骤"""
        if not self._receive_stream:
            return

        try:
            # 获取所有可用消息
            start_time = datetime.now(tz=BotConfig.timezone)
            messages_processed = 0

            while (
                len(self._batch) < self.time_slider.batch_size
                and self._receive_stream.statistics().current_buffer_used > 0
                and (datetime.now(tz=BotConfig.timezone) - start_time).total_seconds()
                < 1.0  # 最多处理1秒
            ):
                try:
                    item = await self._receive_stream.receive()
                    self._batch.append(item)
                    messages_processed += 1
                except ClosedResourceError:
                    break

            # 如果有消息需要处理，则进行处理
            if self._batch:
                await self._flush_current_batch()
                logger.debug(
                    f"处理了 {messages_processed} 条新消息, "
                    f"队列中还有 "
                    f"{self._receive_stream.statistics().current_buffer_used} "
                    f"条待处理"
                )

        except Exception as e:
            logger.error(f"处理队列步骤时发生错误: {e}")

    async def _flush_current_batch(self):
        """刷新并处理当前批次"""
        if not self._batch:
            return

        batch_to_process = self._batch.copy()
        self._batch = []
        self._batch_start_time = datetime.now(tz=BotConfig.timezone)

        process_start = datetime.now(tz=BotConfig.timezone)
        try:
            await self.processor(batch_to_process)
            process_time = (
                datetime.now(tz=BotConfig.timezone) - process_start
            ).total_seconds()
            self.time_slider.record_batch_process(process_time)

            if len(batch_to_process) > 1:
                logger.debug(
                    f"成功处理批次: {len(batch_to_process)}条消息, "
                    f"耗时: {process_time:.3f}s, "
                )
        except Exception as e:
            logger.error(f"批处理失败: {e}")
            await self._retry_batch(batch_to_process)

    async def _parameter_adjustment_task(self):
        """周期性检查并调整队列参数"""
        while self._running:
            try:
                await sleep(self.queue_config.load_check_interval)
                adjusted = self.time_slider.adjust_parameters()
                if adjusted is not None:
                    # 强制触发一次处理
                    self._force_process = True
                    self._new_message_event.set()
            except Exception as e:
                logger.error(f"参数调整任务出错: {e}")
                await sleep(5)

    async def stop(self):
        """停止队列管理器"""
        if not self._running:
            return

        self._running = False

        # 处理剩余的消息
        if self._batch:
            try:
                await self._flush_current_batch()
            except Exception as e:
                logger.error(f"停止时处理剩余批次失败: {e}")

        # 关闭流
        if self._send_stream:
            await self._send_stream.aclose()

        # 取消任务组
        if self._task_group:
            self._task_group.cancel_scope.cancel()

    async def put(self, item: T) -> bool:
        """添加一个项目到队列"""
        if not self._running or not self._send_stream:
            return False

        try:
            await self._send_stream.send(item)
            self.time_slider.record_message()
            # 通知有新消息
            self._new_message_event.set()
            return True
        except ClosedResourceError:
            logger.error("流已关闭")
            return False
        except Exception as e:
            logger.error(f"发送数据失败: {e}")
            return False

    async def _retry_batch(self, batch: list[T]):
        """重试处理失败的批次"""
        start_time = datetime.now(tz=BotConfig.timezone)
        retry_count = 0

        @retry(
            stop=stop_after_attempt(self.queue_config.max_retry),
            retry=retry_if_exception_type(Exception),
            wait=wait_exponential(multiplier=2, min=5, max=30),
            reraise=True,
            sleep=sleep,
        )
        async def _():
            nonlocal retry_count
            try:
                await self.processor(batch)
                return
            except Exception as e:
                retry_count += 1
                elapsed = (
                    datetime.now(tz=BotConfig.timezone) - start_time
                ).total_seconds()
                logger.error(
                    f"批处理重试失败 "
                    f"(尝试 {retry_count}/{self.queue_config.max_retry}, "
                    f"已用时 {elapsed:.2f}s): {e}"
                )
                raise

        try:
            await _()
            if retry_count > 0:
                total_time = (
                    datetime.now(tz=BotConfig.timezone) - start_time
                ).total_seconds()
                logger.info(
                    f"批处理在 {retry_count} 次重试后成功 (耗时 {total_time:.2f}s)"
                )
        except Exception as e:
            total_time = (
                datetime.now(tz=BotConfig.timezone) - start_time
            ).total_seconds()
            logger.error(
                f"批处理在 {retry_count} 次重试后最终失败 (耗时 {total_time:.2f}s): {e}"
            )
            raise

    def get_queue_size(self) -> int:
        """获取当前队列中的消息数量"""
        return len(self._batch) + (
            self._receive_stream.statistics().current_buffer_used
            if self._receive_stream
            else 0
        )


class CacheProvider(Protocol):
    async def get(self, key: str) -> Any:
        """获取缓存值"""
        ...

    async def set(self, key: str, value: Any, expire: int = 0) -> bool:
        """设置缓存值，可选过期时间"""
        ...

    async def delete(self, key: str) -> bool:
        """删除缓存键"""
        ...

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        ...

    async def batch_get(self, keys: list[str]) -> dict[str, Any]:
        """批量获取缓存值"""
        ...

    async def batch_set(self, mapping: dict[str, Any], expire: int = 0) -> bool:
        """批量设置缓存值"""
        ...


# class CacheAwareDecorator(Generic[Entity]):
#     """装饰器类，为数据库处理器添加缓存功能"""
#
#     def __init__(
#         self,
#         processor: Callable,
#         cache_provider: CacheProvider,
#         cache_strategy: CacheStrategy = CacheStrategy.WRITE_THROUGH,
#         cache_key_prefix: str = "",
#         shutdown_timeout: float = 30.0,
#     ):
#         self._initialized = False
#         self.processor = processor
#         self.cache_provider = cache_provider
#         self.cache_strategy = cache_strategy
#         self.cache_key_prefix = cache_key_prefix
#         self.shutdown_timeout = shutdown_timeout
#         self._send_stream: MemoryObjectSendStream | None = None
#         self._receive_stream: MemoryObjectReceiveStream | None = None
#         self._worker_task: TaskStatus | None = None
#         self._task_group: TaskGroup | None = None
#         self._queue_empty_event = Event()
#
#         if cache_strategy == CacheStrategy.WRITE_BEHIND:
#             self._send_stream, self._receive_stream = create_memory_object_stream[
#                 dict[str, Any]
#             ](max_buffer_size=100)
#
#     async def _ensure_initialized(self) -> None:
#         """确保后台任务已初始化"""
#         if not self._initialized and self.cache_strategy == CacheStrategy.WRITE_BEHIND:  # noqa: E501
#             self._task_group = create_task_group()
#             async with self._task_group as tg:
#                 self._worker_task = await tg.start(self._cache_worker)
#             self._initialized = True
#
#     async def __call__(self, batch: list[Entity]) -> None:
#         await self._ensure_initialized()
#         operations = await self.processor._prepare_operations(batch)
#         cache_operations = await self._prepare_cache_operations(operations)
#
#         try:
#             await self.processor(batch)
#
#             if self.cache_strategy != CacheStrategy.WRITE_AROUND:
#                 if self.cache_strategy == CacheStrategy.WRITE_THROUGH:
#                     await self._update_cache(cache_operations)
#                 elif self.cache_strategy == CacheStrategy.WRITE_BEHIND:
#                     await self._queue_cache_updates(cache_operations)
#         except Exception as e:
#             if self.cache_strategy == CacheStrategy.WRITE_THROUGH:
#                 await self._rollback_cache(cache_operations)
#             raise e
#
#     @abstractmethod
#     async def _prepare_cache_operations(
#         self, operations: list[DatabaseOperation]
#     ) -> dict[str, Any]:
#         """子类需要实现缓存操作的准备逻辑"""
#         pass
#
#     async def _update_cache(self, cache_operations: dict[str, Any]) -> None:
#         try:
#             await self.cache_provider.batch_set(cache_operations)
#         except Exception as e:
#             logger.error(f"Cache update failed: {e}")
#             raise e
#
#     async def _queue_cache_updates(self, cache_operations: dict[str, Any]) -> None:
#         if self._send_stream:
#             self._queue_empty_event = Event()
#             await self._send_stream.send(cache_operations)
#
#     async def _rollback_cache(self, cache_operations: dict[str, Any]) -> None:
#         try:
#             keys = list(cache_operations.keys())
#             # await self.cache_provider.batch_delete(keys)
#         except Exception as e:
#             logger.error(f"Cache rollback failed: {e}")
#
#     async def _cache_worker(self) -> None:
#         if not self._receive_stream:
#             return
#
#         async with self._receive_stream:
#             async for cache_operations in self._receive_stream:
#                 try:
#                     await self._update_cache(cache_operations)
#                     if self._receive_stream.statistics().current_buffer_used == 0:
#                         self._queue_empty_event.set()
#                 except Exception as e:
#                     logger.error(f"Async cache update failed: {e}")
#
#     async def wait_until_queue_empty(self) -> bool:
#         """等待直到队列为空或超时"""
#         if not self._receive_stream:
#             return True
#
#         if self._receive_stream.statistics().current_buffer_used == 0:
#             return True
#
#         with move_on_after(self.shutdown_timeout) as scope:
#             await self._queue_empty_event.wait()
#
#         return not scope.cancel_called
#
#     async def close(self) -> None:
#         if self.cache_strategy != CacheStrategy.WRITE_BEHIND:
#             return
#
#         try:
#             if self._send_stream:
#                 await self._send_stream.aclose()
#
#                 receive_stream = self._receive_stream
#                 if receive_stream is not None:
#                     async with receive_stream:
#                         with move_on_after(self.shutdown_timeout) as scope:
#                             if receive_stream.statistics().current_buffer_used > 0:
#                                 await self._queue_empty_event.wait()
#
#                         if scope.cancel_called:
#                             remaining = receive_stream.statistics().current_buffer_used  # noqa: E501
#                             logger.warning(
#                                 f"Shutdown timeout reached with {remaining} "
#                                 f"cache operations remaining"
#                             )
#                         else:
#                             logger.info("All cache operations processed successfully")
#
#         except Exception as e:
#             logger.error(f"Error during graceful shutdown: {e}")


class MessageProcessor:
    def __init__(self):
        self.queue = QueueManager(processor=self.process_messages)

    async def start(self):
        await self.queue.start()

    async def stop(self):
        await self.queue.stop()

    async def add_message(self, message_data) -> bool:
        # 将消息添加到队列
        return await self.queue.put(message_data)

    @staticmethod
    async def process_messages(batch: list[ChatHistory]):
        """批量处理消息并写入数据库"""
        try:
            # 批量创建消息记录
            await ChatHistory.bulk_create(batch)
        except Exception as e:
            logger.error(f"批处理失败: {e}")
            raise
