


from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class DirFile(BaseModel):

  """
  文件或文件夹
  """

  is_file: bool
  """是否为文件"""
  name: str
  """文件夹或文件名称"""
  parent: Optional[str] = None
  """父级"""
