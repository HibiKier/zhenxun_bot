from strenum import StrEnum


class CacheType(StrEnum):
    """
    缓存类型
    """

    PLUGINS = "GLOBAL_ALL_PLUGINS"
    """全局全部插件"""
    GROUPS = "GLOBAL_ALL_GROUPS"
    """全局全部群组"""
    USERS = "GLOBAL_ALL_USERS"
    """全部用户"""
    BAN = "GLOBAL_ALL_BAN"
    """全局ban列表"""
    BOT = "GLOBAL_BOT"
    """全局bot信息"""
    LEVEL = "GLOBAL_USER_LEVEL"
    """用户权限"""


class DbLockType(StrEnum):
    """
    锁类型
    """

    CREATE = "CREATE"
    """创建"""
    DELETE = "DELETE"
    """删除"""
    UPDATE = "UPDATE"
    """更新"""
    QUERY = "QUERY"
    """查询"""


class GoldHandle(StrEnum):
    """
    金币处理
    """

    BUY = "BUY"
    """购买"""
    GET = "GET"
    """获取"""
    PLUGIN = "PLUGIN"
    """插件花费"""


class PropHandle(StrEnum):
    """
    道具处理
    """

    BUY = "BUY"
    """购买"""
    USE = "USE"
    """使用"""


class PluginType(StrEnum):
    """
    插件类型
    """

    SUPERUSER = "SUPERUSER"
    """超级用户"""
    ADMIN = "ADMIN"
    """管理员"""
    SUPER_AND_ADMIN = "ADMIN_SUPER"
    """管理员以及超级用户"""
    NORMAL = "NORMAL"
    """普通插件"""
    DEPENDANT = "DEPENDANT"
    """依赖插件，一般为没有主动触发命令的插件，受权限控制"""
    HIDDEN = "HIDDEN"
    """隐藏插件，一般为没有主动触发命令的插件，不受权限控制，如消息统计"""
    PARENT = "PARENT"
    """父插件，仅仅标记"""


class BlockType(StrEnum):
    """
    禁用状态
    """

    PRIVATE = "PRIVATE"
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
    ALL = "ALL"


class RequestType(StrEnum):
    """
    请求类型
    """

    FRIEND = "FRIEND"
    GROUP = "GROUP"


class RequestHandleType(StrEnum):
    """
    请求处理类型
    """

    APPROVE = "APPROVE"
    """同意"""
    REFUSED = "REFUSED"
    """拒绝"""
    IGNORE = "IGNORE"
    """忽略"""
    EXPIRE = "EXPIRE"
    """过期或失效"""
