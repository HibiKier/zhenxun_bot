from pydantic import BaseModel


class CommonSql(BaseModel):
    sql: str
    """sql语句"""
    remark: str
    """备注"""
