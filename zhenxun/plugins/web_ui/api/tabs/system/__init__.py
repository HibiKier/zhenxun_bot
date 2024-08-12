import os
import shutil
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter

from zhenxun.utils._build_image import BuildImage

from ....base_model import Result
from ....utils import authentication, get_system_disk
from .model import AddFile, DeleteFile, DirFile, RenameFile, SaveFile

router = APIRouter(prefix="/system")

IMAGE_TYPE = ["jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"]


@router.get(
    "/get_dir_list", dependencies=[authentication()], description="获取文件列表"
)
async def _(path: Optional[str] = None) -> Result:
    base_path = Path(path) if path else Path()
    data_list = []
    for file in os.listdir(base_path):
        file_path = base_path / file
        is_image = False
        for t in IMAGE_TYPE:
            if file.endswith(f".{t}"):
                is_image = True
                break
        data_list.append(
            DirFile(
                is_file=not file_path.is_dir(),
                is_image=is_image,
                name=file,
                parent=path,
            )
        )
    return Result.ok(data_list)


@router.get(
    "/get_resources_size", dependencies=[authentication()], description="获取文件列表"
)
async def _(full_path: Optional[str] = None) -> Result:
    return Result.ok(await get_system_disk(full_path))


@router.post("/delete_file", dependencies=[authentication()], description="删除文件")
async def _(param: DeleteFile) -> Result:
    path = Path(param.full_path)
    if not path or not path.exists():
        return Result.warning_("文件不存在...")
    try:
        path.unlink()
        return Result.ok("删除成功!")
    except Exception as e:
        return Result.warning_("删除失败: " + str(e))


@router.post(
    "/delete_folder", dependencies=[authentication()], description="删除文件夹"
)
async def _(param: DeleteFile) -> Result:
    path = Path(param.full_path)
    if not path or not path.exists() or path.is_file():
        return Result.warning_("文件夹不存在...")
    try:
        shutil.rmtree(path.absolute())
        return Result.ok("删除成功!")
    except Exception as e:
        return Result.warning_("删除失败: " + str(e))


@router.post("/rename_file", dependencies=[authentication()], description="重命名文件")
async def _(param: RenameFile) -> Result:
    path = (
        (Path(param.parent) / param.old_name) if param.parent else Path(param.old_name)
    )
    if not path or not path.exists():
        return Result.warning_("文件不存在...")
    try:
        path.rename(path.parent / param.name)
        return Result.ok("重命名成功!")
    except Exception as e:
        return Result.warning_("重命名失败: " + str(e))


@router.post(
    "/rename_folder", dependencies=[authentication()], description="重命名文件夹"
)
async def _(param: RenameFile) -> Result:
    path = (
        (Path(param.parent) / param.old_name) if param.parent else Path(param.old_name)
    )
    if not path or not path.exists() or path.is_file():
        return Result.warning_("文件夹不存在...")
    try:
        new_path = path.parent / param.name
        shutil.move(path.absolute(), new_path.absolute())
        return Result.ok("重命名成功!")
    except Exception as e:
        return Result.warning_("重命名失败: " + str(e))


@router.post("/add_file", dependencies=[authentication()], description="新建文件")
async def _(param: AddFile) -> Result:
    path = (Path(param.parent) / param.name) if param.parent else Path(param.name)
    if path.exists():
        return Result.warning_("文件已存在...")
    try:
        path.open("w")
        return Result.ok("新建文件成功!")
    except Exception as e:
        return Result.warning_("新建文件失败: " + str(e))


@router.post("/add_folder", dependencies=[authentication()], description="新建文件夹")
async def _(param: AddFile) -> Result:
    path = (Path(param.parent) / param.name) if param.parent else Path(param.name)
    if path.exists():
        return Result.warning_("文件夹已存在...")
    try:
        path.mkdir()
        return Result.ok("新建文件夹成功!")
    except Exception as e:
        return Result.warning_("新建文件夹失败: " + str(e))


@router.get("/read_file", dependencies=[authentication()], description="读取文件")
async def _(full_path: str) -> Result:
    path = Path(full_path)
    if not path.exists():
        return Result.warning_("文件不存在...")
    try:
        text = path.read_text(encoding="utf-8")
        return Result.ok(text)
    except Exception as e:
        return Result.warning_("读取文件失败: " + str(e))


@router.post("/save_file", dependencies=[authentication()], description="读取文件")
async def _(param: SaveFile) -> Result:
    path = Path(param.full_path)
    try:
        with path.open("w") as f:
            f.write(param.content)
        return Result.ok("更新成功!")
    except Exception as e:
        return Result.warning_("保存文件失败: " + str(e))


@router.get("/get_image", dependencies=[authentication()], description="读取图片base64")
async def _(full_path: str) -> Result:
    path = Path(full_path)
    if not path.exists():
        return Result.warning_("文件不存在...")
    try:
        return Result.ok(BuildImage.open(path).pic2bs4())
    except Exception as e:
        return Result.warning_("获取图片失败: " + str(e))
