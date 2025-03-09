from dataclasses import dataclass, field
import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from strenum import StrEnum


@dataclass
class QueueConfig:
    """队列配置"""

    batch_size: int = 1000
    """每批次处理的消息数量"""
    flush_interval: float = 60.0
    """刷新间隔（单位：秒）"""
    max_retry: int = 3
    """最大重试次数"""
    max_queue_size: int = 50000
    """队列最大容量"""
    min_batch_size: int = 1
    """最小批处理大小"""
    max_batch_size: int = 5000
    """最大批处理大小"""
    min_flush_interval: float = 10.0
    """最小刷新间隔（单位：秒）"""
    max_flush_interval: float = 300.0
    """最大刷新间隔（单位：秒）"""
    load_check_interval: float = 15.0
    """负载检查间隔（单位：秒）"""
    window_size: int = 300
    """负载窗口大小（单位：秒）"""
    load_thresholds: dict[str, float] = field(
        default_factory=lambda: {"low": 100.0, "high": 1000.0}
    )
    """负载阈值配置"""


class DatabaseType(StrEnum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"


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
