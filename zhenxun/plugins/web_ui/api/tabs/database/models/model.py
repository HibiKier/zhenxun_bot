from pydantic import BaseModel

from zhenxun.utils.plugin_models.base import CommonSql


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
