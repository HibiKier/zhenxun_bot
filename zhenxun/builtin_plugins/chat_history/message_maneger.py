from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta
import logging
from typing import Generic, TypeVar

import anyio
from anyio.abc import TaskGroup
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream

from .types import HealthCheckConfig, QueueConfig, QueueMetrics

T = TypeVar("T")


class QueueHealthCheck:
    """队列健康检查器"""

    def __init__(self, queue_manager: "QueueManager"):
        self.queue = queue_manager
        self.metrics = queue_manager.metrics
        self.config = queue_manager.health_config

    def check_running_status(self) -> bool:
        """检查运行状态"""
        return self.queue.running

    def check_processing_delay(self) -> bool:
        """检查处理延迟"""
        if not self.metrics.last_process_time:
            return True

        delay = (datetime.now() - self.metrics.last_process_time).total_seconds()
        return delay <= self.config.max_delay_seconds

    def check_queue_size(self) -> bool:
        """检查队列大小"""
        return self.metrics.pending_count <= self.config.max_queue_size

    def check_failure_rate(self) -> bool:
        """检查失败率"""
        if self.metrics.total_processed == 0:
            return True
        return self.metrics.failure_rate <= self.config.max_failure_rate

    def is_healthy(self) -> bool:
        """执行所有健康检查"""
        return all(
            [
                self.check_running_status(),
                self.check_processing_delay(),
                self.check_queue_size(),
                self.check_failure_rate(),
            ]
        )


class QueueManager(Generic[T]):
    def __init__(
        self,
        processor: Callable[[list[T]], Awaitable[None]],
        config: QueueConfig = QueueConfig(),
        health_config: HealthCheckConfig = HealthCheckConfig(),
    ):
        self.config = config
        self.health_config = health_config
        self.processor = processor
        self.metrics = QueueMetrics(batch_size=config.batch_size)
        self._health_checker = QueueHealthCheck(self)
        self._send_stream: MemoryObjectSendStream[T] | None = None
        self._receive_stream: MemoryObjectReceiveStream[T] | None = None
        self._running = False
        self._tasks: set[TaskGroup] = set()
        self._last_process_time: datetime | None = None

    async def start(self):
        """Start the queue manager"""
        if self._running:
            return

        self._send_stream, self._receive_stream = anyio.create_memory_object_stream(
            max_buffer_size=self.config.max_queue_size
        )
        self._running = True

        async with anyio.create_task_group() as tg:
            self._tasks.add(tg)
            tg.start_soon(self._process_queue)
            tg.start_soon(self._monitor_performance)

    async def stop(self):
        """Stop the queue manager"""
        if not self._running:
            return

        self._running = False
        if self._send_stream:
            await self._send_stream.aclose()

        for tg in self._tasks:
            tg.cancel_scope.cancel()
        self._tasks.clear()

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
        batch_start_time = datetime.now()

        async for item in self._receive_stream:
            batch.append(item)

            if (
                len(batch) >= self.config.batch_size
                or (datetime.now() - batch_start_time).total_seconds()
                >= self.config.flush_interval
            ):
                await self._process_batch(batch)
                batch = []
                batch_start_time = datetime.now()

    async def _process_batch(self, batch: list[T]):
        """Process a batch of items"""
        if not batch:
            return

        start_time = datetime.now()
        try:
            await self.processor(batch)
            self.metrics.processed_count += len(batch)
            process_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(len(batch), process_time)
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

    def _update_metrics(self, processed_count: int, process_time: float):
        """Update queue metrics"""
        current_time = datetime.now()
        self.metrics.last_process_time = current_time
        self._last_process_time = current_time

        if processed_count > 0:
            self.metrics.avg_process_time = (
                self.metrics.avg_process_time
                * (self.metrics.processed_count - processed_count)
                + process_time * processed_count
            ) / self.metrics.processed_count

    @property
    def is_healthy(self) -> bool:
        """检查队列健康状态"""
        return self._health_checker.is_healthy()

    @property
    def running(self):
        return self._running
