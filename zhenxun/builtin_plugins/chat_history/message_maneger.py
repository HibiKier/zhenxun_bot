from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import sys
from typing import Any, Generic, Protocol, TypeVar

import anyio
from anyio import Event, create_memory_object_stream, create_task_group, move_on_after
from anyio.abc import TaskGroup, TaskStatus
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream

from zhenxun.configs.config import BotConfig
from zhenxun.services.log import logger

from .types import QueueConfig, QueueMetrics

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum

T = TypeVar("T")
Entity = TypeVar("Entity")
Row = TypeVar("Row")


class QueueManager(Generic[T]):
    def __init__(
        self,
        processor: Callable[[list[T]], Awaitable[None]],
        config: QueueConfig = QueueConfig(),
    ):
        self.config = config
        self.processor = processor
        self.metrics = QueueMetrics(batch_size=config.batch_size)
        self._send_stream: MemoryObjectSendStream[T] | None = None
        self._receive_stream: MemoryObjectReceiveStream[T] | None = None
        self._running = False
        self._last_process_time: datetime | None = None

    async def start(self) -> None:
        """Start the queue manager"""
        if self._running:
            return

        self._send_stream, self._receive_stream = anyio.create_memory_object_stream(
            max_buffer_size=self.config.max_queue_size
        )
        self._running = True

        async with anyio.create_task_group():
            with move_on_after(1) as scope:
                await self._process_queue()
            if scope.cancel_called:
                logging.error("Queue processing failed due to timeout")

    async def stop(self):
        """Stop the queue manager"""
        if not self._running:
            return

        self._running = False
        if self._send_stream:
            await self._send_stream.aclose()

    async def put(self, item: T) -> bool:
        """Add an item to the queue"""
        if not self._running or not self._send_stream:
            return False

        try:
            await self._send_stream.send(item)
            self.metrics.pending_count += 1
            current_time = datetime.now()
            self.metrics._message_times.append(current_time)
            return True
        except anyio.ClosedResourceError:
            return False

    async def _process_queue(self):
        """Process items in the queue"""
        if not self._receive_stream:
            return

        batch: list[T] = []
        batch_start_time = datetime.now(tz=BotConfig.timezone)

        async for item in self._receive_stream:
            batch.append(item)

            if (
                len(batch) >= self.config.batch_size
                or (
                    datetime.now(tz=BotConfig.timezone) - batch_start_time
                ).total_seconds()
                >= self.config.flush_interval
            ):
                # 批大小达到阈值或者刷新间隔到达阈值时处理并清空
                await self._process_batch(batch)
                batch = []
                batch_start_time = datetime.now()

    async def _process_batch(self, batch: list[T]):
        """Process a batch of items"""
        if not batch:
            return

        try:
            await self.processor(batch)
            self.metrics.processed_count += len(batch)
        except Exception as e:
            logging.error(f"Batch processing failed: {e}")
            self.metrics.failed_count += len(batch)
            await self._retry_batch(batch)

    async def _retry_batch(self, batch: list[T]):
        """Retry processing failed batch"""
        for retry in range(self.config.max_retry):
            try:
                await anyio.sleep(2**retry)  # Exponential backoff
                await self.processor(batch)
                return
            except Exception as e:
                self.metrics.retry_count += 1
                logging.error(f"Retry {retry + 1} failed: {e}")

    async def _monitor_performance(self):
        """Monitor queue performance and adjust parameters"""
        while self._running:
            await anyio.sleep(self.config.load_check_interval)
            self._adjust_queue_parameters()

    def _adjust_queue_parameters(self):
        """调整队列参数基于性能指标"""
        # 移除未使用的 current_time
        message_rate = self._calculate_message_rate()

        # 基于消息率计算负载水平
        load_level = (message_rate - self.config.load_thresholds["low"]) / (
            self.config.load_thresholds["high"] - self.config.load_thresholds["low"]
        )
        load_level = max(0.0, min(1.0, load_level))

        # 动态调整批处理大小
        new_batch_size = int(
            self.config.min_batch_size
            + (self.config.max_batch_size - self.config.min_batch_size) * load_level
        )
        self.config.batch_size = new_batch_size

    def _calculate_message_rate(self) -> float:
        """Calculate current message processing rate"""
        current_time = datetime.now()
        window_start = current_time - timedelta(seconds=self.config.window_size)

        recent_messages = sum(t >= window_start for t in self.metrics._message_times)
        minutes = self.config.window_size / 60

        return recent_messages / minutes if minutes > 0 else 0

    @property
    def running(self):
        return self._running


class DatabaseOperationType(StrEnum):
    """
    数据库操作类型

    - INSERT: 插入
    - UPDATE: 更新
    - DELETE: 删除
    - UPSERT: 更新或插入
    """

    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    UPSERT = "upsert"


class CacheStrategy(StrEnum):
    """
    缓存策略

    - WRITE_THROUGH: 同步写入
    - WRITE_BEHIND: 异步写入
    - WRITE_AROUND: 跳过缓存
    """

    WRITE_THROUGH = "write_through"
    WRITE_BEHIND = "write_behind"
    WRITE_AROUND = "write_around"


@dataclass
class DatabaseOperation:
    type: DatabaseOperationType
    data: dict


class BaseDatabaseProcessor(ABC, Generic[Row]):
    def __init__(self):
        self._connection = None
        self._transaction = None

    @abstractmethod
    async def begin_transaction(self) -> None:
        """开始事务"""
        pass

    @abstractmethod
    async def commit_transaction(self) -> None:
        """提交事务"""
        pass

    @abstractmethod
    async def rollback_transaction(self) -> None:
        """回滚事务"""
        pass

    @abstractmethod
    async def execute_batch(self, operations: list[DatabaseOperation]) -> None:
        """执行批量操作"""
        pass

    async def __call__(self, batch: list[Row]) -> None:
        """
        实现QueueManager的processor接口
        """
        try:
            operations = await self._prepare_operations(batch)

            await self.begin_transaction()
            try:
                await self.execute_batch(operations)
                await self.commit_transaction()
            except Exception as e:
                await self.rollback_transaction()
                raise e

        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            raise e

    @abstractmethod
    async def _prepare_operations(self, batch: list[Row]) -> list[DatabaseOperation]:
        """
        将输入数据转换为数据库操作
        子类需要实现此方法来定义如何将输入数据转换为具体的数据库操作
        """
        pass

    async def _validate_batch(self, batch: list[Row]) -> bool:
        """
        验证批量数据的有效性
        子类可以重写此方法来实现特定的验证逻辑
        """
        return True


class CacheProvider(Protocol):
    async def set(self, key: str, value: Any, expire: int | None = None) -> None: ...

    async def get(self, key: str) -> Any | None: ...

    async def delete(self, key: str) -> None: ...

    async def batch_set(self, items: dict[str, Any]) -> None: ...

    async def batch_delete(self, keys: list[str]) -> None: ...


class CacheAwareDecorator(Generic[Entity]):
    """装饰器类，为数据库处理器添加缓存功能"""

    def __init__(
        self,
        processor: BaseDatabaseProcessor[Entity],
        cache_provider: CacheProvider,
        cache_strategy: CacheStrategy = CacheStrategy.WRITE_THROUGH,
        cache_key_prefix: str = "",
        shutdown_timeout: float = 30.0,
    ):
        self._initialized = False
        self.processor = processor
        self.cache_provider = cache_provider
        self.cache_strategy = cache_strategy
        self.cache_key_prefix = cache_key_prefix
        self.shutdown_timeout = shutdown_timeout
        self._send_stream: MemoryObjectSendStream | None = None
        self._receive_stream: MemoryObjectReceiveStream | None = None
        self._worker_task: TaskStatus | None = None
        self._task_group: TaskGroup | None = None
        self._queue_empty_event = Event()

        if cache_strategy == CacheStrategy.WRITE_BEHIND:
            self._send_stream, self._receive_stream = create_memory_object_stream[
                dict[str, Any]
            ](max_buffer_size=100)

    async def _ensure_initialized(self) -> None:
        """确保后台任务已初始化"""
        if not self._initialized and self.cache_strategy == CacheStrategy.WRITE_BEHIND:
            self._task_group = create_task_group()
            async with self._task_group as tg:
                self._worker_task = await tg.start(self._cache_worker)
            self._initialized = True

    async def __call__(self, batch: list[Entity]) -> None:
        await self._ensure_initialized()
        operations = await self.processor._prepare_operations(batch)
        cache_operations = await self._prepare_cache_operations(operations)

        try:
            await self.processor(batch)

            if self.cache_strategy != CacheStrategy.WRITE_AROUND:
                if self.cache_strategy == CacheStrategy.WRITE_THROUGH:
                    await self._update_cache(cache_operations)
                elif self.cache_strategy == CacheStrategy.WRITE_BEHIND:
                    await self._queue_cache_updates(cache_operations)
        except Exception as e:
            if self.cache_strategy == CacheStrategy.WRITE_THROUGH:
                await self._rollback_cache(cache_operations)
            raise e

    @abstractmethod
    async def _prepare_cache_operations(
        self, operations: list[DatabaseOperation]
    ) -> dict[str, Any]:
        """子类需要实现缓存操作的准备逻辑"""
        pass

    async def _update_cache(self, cache_operations: dict[str, Any]) -> None:
        try:
            await self.cache_provider.batch_set(cache_operations)
        except Exception as e:
            logger.error(f"Cache update failed: {e}")
            raise e

    async def _queue_cache_updates(self, cache_operations: dict[str, Any]) -> None:
        if self._send_stream:
            self._queue_empty_event = Event()
            await self._send_stream.send(cache_operations)

    async def _rollback_cache(self, cache_operations: dict[str, Any]) -> None:
        try:
            keys = list(cache_operations.keys())
            await self.cache_provider.batch_delete(keys)
        except Exception as e:
            logger.error(f"Cache rollback failed: {e}")

    async def _cache_worker(self) -> None:
        if not self._receive_stream:
            return

        async with self._receive_stream:
            async for cache_operations in self._receive_stream:
                try:
                    await self._update_cache(cache_operations)
                    if self._receive_stream.statistics().current_buffer_used == 0:
                        self._queue_empty_event.set()
                except Exception as e:
                    logger.error(f"Async cache update failed: {e}")

    async def wait_until_queue_empty(self) -> bool:
        """等待直到队列为空或超时"""
        if not self._receive_stream:
            return True

        if self._receive_stream.statistics().current_buffer_used == 0:
            return True

        with move_on_after(self.shutdown_timeout) as scope:
            await self._queue_empty_event.wait()

        return not scope.cancel_called

    async def close(self) -> None:
        if self.cache_strategy != CacheStrategy.WRITE_BEHIND:
            return

        try:
            if self._send_stream:
                await self._send_stream.aclose()

                receive_stream = self._receive_stream
                if receive_stream is not None:
                    async with receive_stream:
                        with move_on_after(self.shutdown_timeout) as scope:
                            if receive_stream.statistics().current_buffer_used > 0:
                                await self._queue_empty_event.wait()

                        if scope.cancel_called:
                            remaining = receive_stream.statistics().current_buffer_used
                            logger.warning(
                                f"Shutdown timeout reached with {remaining} "
                                f"cache operations remaining"
                            )
                        else:
                            logger.info("All cache operations processed successfully")

        except Exception as e:
            logger.error(f"Error during graceful shutdown: {e}")
