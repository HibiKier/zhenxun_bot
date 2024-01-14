import os
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter

from ....base_model import Result
from ....utils import authentication, get_system_disk
from .model import DirFile

router = APIRouter(prefix="/system")



@router.get("/get_dir_list", dependencies=[authentication()], description="获取文件列表")
async def _(path: Optional[str] = None) -> Result:
  base_path = Path(path) if path else Path()
  data_list = []
  for file in os.listdir(base_path):
    data_list.append(DirFile(is_file=not (base_path / file).is_dir(), name=file, parent=path))
  return Result.ok(data_list)


@router.get("/get_resources_size", dependencies=[authentication()], description="获取文件列表")
async def _(type: Optional[str] = None) -> Result:
  return Result.ok(await get_system_disk(type))