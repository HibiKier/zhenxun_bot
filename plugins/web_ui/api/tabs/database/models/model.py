from typing import List

from pydantic import BaseModel

from utils.models import CommonSql


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
    plugin_name: str
    """插件名称"""
    sql_list: List[CommonSql]
    """插件列表"""
