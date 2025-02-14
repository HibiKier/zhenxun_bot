from pydantic import BaseModel

from zhenxun.utils.plugin_models.base import CommonSql


class SqlLogInfo(BaseModel):
    sql: str
    """sql语句"""


class SqlText(BaseModel):
    """
    sql语句
    """

    sql: str


class SqlModel(BaseModel):
    """
    常用sql
    """

    name: str
    """插件中文名称"""
    module: str
    """插件名称"""
    sql_list: list[CommonSql]
    """插件列表"""


class Column(BaseModel):
    """
    列
    """

    column_name: str
    """列名"""
    data_type: str
    """数据类型"""
    max_length: int | None
    """最大长度"""
    is_nullable: str
    """是否可为空"""
