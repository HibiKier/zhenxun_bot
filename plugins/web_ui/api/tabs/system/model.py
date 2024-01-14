


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

class SystemFolderSize(BaseModel):
    """
    资源文件占比
    """

    font_dir_size: float
    image_dir_size: float
    text_dir_size: float
    record_dir_size: float
    temp_dir_size: float
    data_dir_size: float
    log_dir_size: float
    check_time: datetime