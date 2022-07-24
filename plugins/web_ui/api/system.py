import asyncio
import os
from pathlib import Path

import psutil
import ujson as json
from configs.path_config import (
    DATA_PATH,
    FONT_PATH,
    IMAGE_PATH,
    LOG_PATH,
    RECORD_PATH,
    TEMP_PATH,
    TEXT_PATH,
)
from services.log import logger
from utils.http_utils import AsyncHttpx

from ..auth import Depends, User, token_to_user
from ..config import *

CPU_DATA_PATH = DATA_PATH / "system" / "cpu.json"
MEMORY_DATA_PATH = DATA_PATH / "system" / "memory.json"
DISK_DATA_PATH = DATA_PATH / "system" / "disk.json"
CPU_DATA_PATH.parent.mkdir(exist_ok=True, parents=True)
cpu_data = {"data": []}
memory_data = {"data": []}
disk_data = {"data": []}


@app.get("/webui/system")
async def _() -> Result:
    return await get_system_data()


@app.get("/webui/system/status")
async def _(user: User = Depends(token_to_user)) -> Result:
    return Result(
        code=200,
        data=await asyncio.get_event_loop().run_in_executor(None, _get_system_status),
    )


@app.get("/webui/system/disk")
async def _(type_: Optional[str] = None, user: User = Depends(token_to_user)) -> Result:
    return Result(
        code=200,
        data=await asyncio.get_event_loop().run_in_executor(
            None, _get_system_disk, type_
        ),
    )


@app.get("/webui/system/statusList")
async def _(user: User = Depends(token_to_user)) -> Result:
    global cpu_data, memory_data, disk_data
    await asyncio.get_event_loop().run_in_executor(None, _get_system_status)
    cpu_rst = cpu_data["data"][-10:] if len(cpu_data["data"]) > 10 else cpu_data["data"]
    memory_rst = (
        memory_data["data"][-10:]
        if len(memory_data["data"]) > 10
        else memory_data["data"]
    )
    disk_rst = (
        disk_data["data"][-10:] if len(disk_data["data"]) > 10 else disk_data["data"]
    )
    return Result(
        code=200,
        data=SystemStatusList(
            cpu_data=cpu_rst,
            memory_data=memory_rst,
            disk_data=disk_rst,
        ),
    )


async def get_system_data(user: User = Depends(token_to_user)):
    """
    说明:
        获取系统信息，资源文件大小，网络状态等
    """
    baidu = 200
    google = 200
    try:
        await AsyncHttpx.get("https://www.baidu.com/", timeout=5)
    except Exception as e:
        logger.warning(f"访问BaiDu失败... {type(e)}: {e}")
        baidu = 404
    try:
        await AsyncHttpx.get("https://www.google.com/", timeout=5)
    except Exception as e:
        logger.warning(f"访问Google失败... {type(e)}: {e}")
        google = 404
    network = SystemNetwork(baidu=baidu, google=google)
    disk = await asyncio.get_event_loop().run_in_executor(None, _get_system_disk, None)
    status = await asyncio.get_event_loop().run_in_executor(None, _get_system_status)
    return Result(
        code=200,
        data=SystemResult(
            status=status,
            network=network,
            disk=disk,
            check_time=datetime.now().replace(microsecond=0),
        ),
    )


def _get_system_status(user: User = Depends(token_to_user)) -> SystemStatus:
    """
    说明:
        获取系统信息等
    """
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    save_system_data(cpu, memory, disk)
    return SystemStatus(
        cpu=cpu,
        memory=memory,
        disk=disk,
        check_time=datetime.now().replace(microsecond=0),
    )


def _get_system_disk(
    type_: Optional[str], user: User = Depends(token_to_user)
) -> Union[SystemFolderSize, Dict[str, Union[float, datetime]]]:
    """
    说明:
        获取资源文件大小等
    """
    if not type_:
        disk = SystemFolderSize(
            font_dir_size=_get_dir_size(FONT_PATH) / 1024 / 1024,
            image_dir_size=_get_dir_size(IMAGE_PATH) / 1024 / 1024,
            text_dir_size=_get_dir_size(TEXT_PATH) / 1024 / 1024,
            record_dir_size=_get_dir_size(RECORD_PATH) / 1024 / 1024,
            temp_dir_size=_get_dir_size(TEMP_PATH) / 1024 / 102,
            data_dir_size=_get_dir_size(DATA_PATH) / 1024 / 1024,
            log_dir_size=_get_dir_size(LOG_PATH) / 1024 / 1024,
            check_time=datetime.now().replace(microsecond=0),
        )
        return disk
    else:
        if type_ == "image":
            dir_path = IMAGE_PATH
        elif type_ == "font":
            dir_path = FONT_PATH
        elif type_ == "text":
            dir_path = TEXT_PATH
        elif type_ == "record":
            dir_path = RECORD_PATH
        elif type_ == "data":
            dir_path = DATA_PATH
        elif type_ == "temp":
            dir_path = TEMP_PATH
        else:
            dir_path = LOG_PATH
        dir_map = {}
        other_file_size = 0
        for file in os.listdir(dir_path):
            file = Path(dir_path / file)
            if file.is_dir():
                dir_map[file.name] = _get_dir_size(file) / 1024 / 1024
            else:
                other_file_size += os.path.getsize(file) / 1024 / 1024
        dir_map["其他文件"] = other_file_size
        dir_map["check_time"] = datetime.now().replace(microsecond=0)
        return dir_map


def _get_dir_size(dir_path: Path) -> float:
    """
    说明:
        获取文件夹大小
    参数:
        :param dir_path: 文件夹路径
    """
    size = 0
    for root, dirs, files in os.walk(dir_path):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size


def save_system_data(cpu: float, memory: float, disk: float):
    """
    说明:
        保存一些系统信息
    参数:
        :param cpu: cpu
        :param memory: memory
        :param disk: disk
    """
    global cpu_data, memory_data, disk_data
    if CPU_DATA_PATH.exists() and not cpu_data["data"]:
        with open(CPU_DATA_PATH, "r") as f:
            cpu_data = json.load(f)
    if MEMORY_DATA_PATH.exists() and not memory_data["data"]:
        with open(MEMORY_DATA_PATH, "r") as f:
            memory_data = json.load(f)
    if DISK_DATA_PATH.exists() and not disk_data["data"]:
        with open(DISK_DATA_PATH, "r") as f:
            disk_data = json.load(f)
    now = str(datetime.now().time().replace(microsecond=0))
    cpu_data["data"].append({"time": now, "data": cpu})
    memory_data["data"].append({"time": now, "data": memory})
    disk_data["data"].append({"time": now, "data": disk})
    if len(cpu_data["data"]) > 50:
        cpu_data["data"] = cpu_data["data"][-50:]
    if len(memory_data["data"]) > 50:
        memory_data["data"] = memory_data["data"][-50:]
    if len(disk_data["data"]) > 50:
        disk_data["data"] = disk_data["data"][-50:]
    with open(CPU_DATA_PATH, "w") as f:
        json.dump(cpu_data, f, indent=4, ensure_ascii=False)
    with open(MEMORY_DATA_PATH, "w") as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)
    with open(DISK_DATA_PATH, "w") as f:
        json.dump(disk_data, f, indent=4, ensure_ascii=False)
