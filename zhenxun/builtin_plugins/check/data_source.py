from dataclasses import dataclass
import os
from pathlib import Path
import platform
import subprocess

import cpuinfo
import nonebot
from nonebot.utils import run_sync
import psutil
from pydantic import BaseModel

from zhenxun.configs.config import BotConfig
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx

BAIDU_URL = "https://www.baidu.com/"
GOOGLE_URL = "https://www.google.com/"

VERSION_FILE = Path() / "__version__"
ARM_KEY = "aarch64"


@dataclass
class CPUInfo:
    core: int | None
    """CPU 物理核心数"""
    usage: float
    """CPU 占用百分比，取值范围(0,100]"""
    freq: float
    """CPU 的时钟速度（单位：GHz）"""

    @classmethod
    def get_cpu_info(cls):
        cpu_core = psutil.cpu_count(logical=False)
        cpu_usage = psutil.cpu_percent(interval=0.1)
        if _cpu_freq := psutil.cpu_freq():
            cpu_freq = round(_cpu_freq.current / 1000, 2)
        else:
            cpu_freq = 0
        return CPUInfo(core=cpu_core, usage=cpu_usage, freq=cpu_freq)


@dataclass
class RAMInfo:
    """RAM 信息（单位：GB）"""

    total: float
    """RAM 总量"""
    usage: float
    """当前 RAM 占用量/GB"""

    @classmethod
    def get_ram_info(cls):
        ram_total = round(psutil.virtual_memory().total / (1024**3), 2)
        ram_usage = round(psutil.virtual_memory().used / (1024**3), 2)

        return RAMInfo(total=ram_total, usage=ram_usage)


@dataclass
class SwapMemory:
    """Swap 信息（单位：GB）"""

    total: float
    """Swap 总量"""
    usage: float
    """当前 Swap 占用量/GB"""

    @classmethod
    def get_swap_info(cls):
        swap_total = round(psutil.swap_memory().total / (1024**3), 2)
        swap_usage = round(psutil.swap_memory().used / (1024**3), 2)

        return SwapMemory(total=swap_total, usage=swap_usage)


@dataclass
class DiskInfo:
    """硬盘信息"""

    total: float
    """硬盘总量"""
    usage: float
    """当前硬盘占用量/GB"""

    @classmethod
    def get_disk_info(cls):
        disk_total = round(psutil.disk_usage("/").total / (1024**3), 2)
        disk_usage = round(psutil.disk_usage("/").used / (1024**3), 2)

        return DiskInfo(total=disk_total, usage=disk_usage)


class SystemInfo(BaseModel):
    """系统信息"""

    cpu: CPUInfo
    """CPU信息"""
    ram: RAMInfo
    """RAM信息"""
    swap: SwapMemory
    """SWAP信息"""
    disk: DiskInfo
    """DISK信息"""

    def get_system_info(self):
        return {
            "cpu_info": f"{self.cpu.usage}% - {self.cpu.freq}Ghz "
            f"[{self.cpu.core} core]",
            "cpu_process": self.cpu.usage,
            "ram_info": f"{self.ram.usage} / {self.ram.total} GB",
            "ram_process": (
                0 if self.ram.total == 0 else (self.ram.usage / self.ram.total * 100)
            ),
            "swap_info": f"{self.swap.usage} / {self.swap.total} GB",
            "swap_process": (
                0 if self.swap.total == 0 else (self.swap.usage / self.swap.total * 100)
            ),
            "disk_info": f"{self.disk.usage} / {self.disk.total} GB",
            "disk_process": (
                0 if self.disk.total == 0 else (self.disk.usage / self.disk.total * 100)
            ),
        }


@run_sync
def __build_status() -> SystemInfo:
    """获取 `CPU` `RAM` `SWAP` `DISK` 信息"""
    cpu = CPUInfo.get_cpu_info()
    ram = RAMInfo.get_ram_info()
    swap = SwapMemory.get_swap_info()
    disk = DiskInfo.get_disk_info()

    return SystemInfo(cpu=cpu, ram=ram, swap=swap, disk=disk)


async def __get_network_info():
    """网络请求"""
    baidu, google = True, True
    try:
        await AsyncHttpx.get(BAIDU_URL, timeout=5)
    except Exception as e:
        logger.warning("自检：百度无法访问...", e=e)
        baidu = False
    try:
        await AsyncHttpx.get(GOOGLE_URL, timeout=5)
    except Exception as e:
        logger.warning("自检：谷歌无法访问...", e=e)
        google = False
    return baidu, google


def __get_version() -> str | None:
    """获取版本信息"""
    if VERSION_FILE.exists():
        with open(VERSION_FILE, encoding="utf-8") as f:
            if text := f.read():
                return text.split(":")[-1]
    return None


def __get_arm_cpu():
    env = os.environ.copy()
    env["LC_ALL"] = "en_US.UTF-8"
    cpu_info = subprocess.check_output(["lscpu"], env=env).decode()
    model_name = ""
    cpu_freq = 0
    for line in cpu_info.splitlines():
        if "Model name" in line:
            model_name = line.split(":")[1].strip()
        if "CPU MHz" in line:
            cpu_freq = float(line.split(":")[1].strip())
    return model_name, cpu_freq


def __get_arm_oracle_cpu_freq():
    cpu_freq = subprocess.check_output(
        ["dmidecode", "-s", "processor-frequency"]
    ).decode()
    return round(float(cpu_freq.split()[0]) / 1000, 2)


async def get_status_info() -> dict:
    """获取信息"""
    data = await __build_status()

    system = platform.uname()
    if system.machine == ARM_KEY and not (
        cpuinfo.get_cpu_info().get("brand_raw") and data.cpu.freq
    ):
        model_name, cpu_freq = __get_arm_cpu()
        if not data.cpu.freq:
            data.cpu.freq = cpu_freq or __get_arm_oracle_cpu_freq()
        data = data.get_system_info()
        data["brand_raw"] = model_name
    else:
        data = data.get_system_info()
        data["brand_raw"] = cpuinfo.get_cpu_info().get("brand_raw", "Unknown")

    baidu, google = await __get_network_info()
    data["baidu"] = "#8CC265" if baidu else "red"
    data["google"] = "#8CC265" if google else "red"

    data["system"] = f"{system.system} {system.release}"
    data["version"] = __get_version()
    data["plugin_count"] = len(nonebot.get_loaded_plugins())
    data["nickname"] = BotConfig.self_nickname
    return data
