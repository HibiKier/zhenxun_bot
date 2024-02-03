from strenum import StrEnum


class PluginType(StrEnum):
    """
    插件类型
    """

    SUPERUSER = "超级管理员插件"
    ADMIN = "管理员插件"
    NORMAL = "普通插件"
    HIDDEN = "被动插件"


class BlockType(StrEnum):
    """
    禁用状态
    """

    FRIEND = "PRIVATE"
    GROUP = "GROUP"
    ALL = "ALL"


class PluginLimitType(StrEnum):
    """
    插件限制类型
    """

    CD = "CD"
    COUNT = "COUNT"
    BLOCK = "BLOCK"


class LimitCheckType(StrEnum):
    """
    插件限制类型
    """

    PRIVATE = "PRIVATE"
    GROUP = "GROUP"
    ALL = "ALL"


class LimitWatchType(StrEnum):
    """
    插件限制监听对象
    """

    USER = "USER"
    GROUP = "GROUP"


class RequestType(StrEnum):
    """
    请求类型
    """

    FRIEND = "FRIEND"
    GROUP = "GROUP"


class RequestHandleType(StrEnum):
    """
    请求类型
    """

    APPROVE = "APPROVE"
    """同意"""
    REFUSED = "REFUSED"
    """拒绝"""
    IGNORE = "IGNORE"
    """忽略"""
