from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar

T = TypeVar("T")


@dataclass
class QueueMetrics:
    """Queue performance metrics"""

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
        return self.processed_count + self.failed_count

    @property
    def failure_rate(self) -> float:
        return (
            self.failed_count / self.total_processed
            if self.total_processed > 0
            else 0.0
        )


@dataclass
class QueueConfig:
    """Queue configuration settings"""

    batch_size: int = 1000
    flush_interval: float = 60.0
    max_retry: int = 3
    max_queue_size: int = 50000
    min_batch_size: int = 100
    max_batch_size: int = 5000
    min_flush_interval: float = 30.0
    max_flush_interval: float = 300.0
    load_check_interval: float = 30.0
    window_size: int = 300
    load_thresholds: dict[str, float] = field(
        default_factory=lambda: {"low": 100.0, "high": 1000.0}
    )


@dataclass
class HealthCheckConfig:
    """Health check configuration"""

    max_delay_seconds: float = 60.0
    max_queue_size: int = 10000
    max_failure_rate: float = 0.1
    max_retry_count: int = 100
    max_load: float = 0.9
