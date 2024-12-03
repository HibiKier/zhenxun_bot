from pydantic import BaseModel


class Barh(BaseModel):
    category_data: list[str]
    """坐标轴数据"""
    data: list[int | float]
    """实际数据"""
    title: str
    """标题"""
