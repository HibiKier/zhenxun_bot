import asyncio
import os
import socket
import sys
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import Literal, TextIO
from collections.abc import AsyncIterator
from urllib.parse import urlparse

from nonebot.log import logger
from playwright.async_api import Browser, Error, Page, Playwright, async_playwright

from .config import plugin_config


@dataclass
class MirrorSource:
    name: str
    url: str
    priority: int


_browser: Browser | None = None
_playwright: Playwright | None = None
BrowserType = Literal["chromium", "firefox", "webkit"]
MIRRORS = [
    MirrorSource("官方", "https://playwright.azureedge.net/builds/", 0),
    MirrorSource("淘宝", "https://npmmirror.com/mirrors/playwright", 1),
]


class PlaywrightInstallError(Exception):
    """Playwright 安装错误"""

    pass


@contextmanager
def _suppress_and_log():
    """抑制并记录关闭期间的任何异常。"""
    try:
        yield
    except Exception as e:
        logger.opt(exception=e).warning("关闭 playwright 时发生错误。")


async def init_browser(**kwargs) -> Browser:
    """初始化全局 playwright 浏览器实例并返回浏览器实例。"""
    try:
        return await start_browser(**kwargs)
    except Error as e:
        logger.error("浏览器初始化失败，尝试安装浏览器中")
        if await install_browser():
            return await start_browser(**kwargs)
        raise RuntimeError("浏览器初始化失败") from e


async def start_browser(**kwargs) -> Browser:
    """
    启动 playwright 浏览器实例。
    Args:
        **kwargs (Any): 传递给 `playwright.launch` 的关键字参数。

    Returns:
        Browser: 浏览器实例。
    """
    global _browser, _playwright
    browser_type = (
        plugin_config.htmlrender_browser.lower()
        if plugin_config.htmlrender_browser
        else "chromium"
    )

    if plugin_config.htmlrender_browser_channel:
        kwargs["channel"] = plugin_config.htmlrender_browser_channel

    if plugin_config.htmlrender_proxy_host:
        kwargs["proxy"] = {
            "server": plugin_config.htmlrender_proxy_host,
        }

    _playwright = await async_playwright().start()

    match browser_type:
        case "firefox":
            logger.info("使用 Firefox 启动中...")
            _browser = await _playwright.firefox.launch(**kwargs)
            logger.debug(f"Firefox 路径: {_playwright.firefox.executable_path}")

        case "webkit":
            logger.info("使用 WebKit 启动中...")
            _browser = await _playwright.webkit.launch(**kwargs)
            logger.debug(f"WebKit 路径: {_playwright.webkit.executable_path}")

        case "chromium":
            if plugin_config.htmlrender_connect_over_cdp:
                logger.info("使用 Chromium CDP 连接中...")
                return await _playwright.chromium.connect_over_cdp(**kwargs)

            logger.info("使用 Chromium 启动中...")
            _browser = await _playwright.chromium.launch(**kwargs)
            logger.debug(f"Chromium 路径: {_playwright.chromium.executable_path}")

        case _:
            raise ValueError(f"不支持的浏览器类型: {browser_type}")

    return _browser


def get_browser() -> Browser:
    """"""
    if not _browser:
        raise RuntimeError("浏览器未初始化")
    return _browser


@asynccontextmanager
async def get_new_page(device_scale_factor: float = 2, **kwargs) -> AsyncIterator[Page]:
    """
    获取一个新的页面的上下文管理器。
    Args:
        device_scale_factor (float): 设备缩放因子。
        **kwargs (Any): 传递给 `browser.new_context` 的关键字参数。

    Returns:
        AsyncIterator[Page]: 页面对象。
    """
    ctx = get_browser()
    page = await ctx.new_page(device_scale_factor=device_scale_factor, **kwargs)
    try:
        yield page
    finally:
        await page.close()


async def shutdown_browser() -> None:
    """关闭浏览器实例。"""
    if _browser:
        with _suppress_and_log():
            await _browser.close()
    if _playwright:
        with _suppress_and_log():
            await _playwright.stop()


async def check_mirror_connectivity(
    mirrors: list[MirrorSource], timeout: int = 5
) -> MirrorSource | None:
    """
    检查镜像源的可用性并返回最佳镜像源。
    Args:
        mirrors (list[MirrorSource]): 镜像源列表。
        timeout (int): 连接超时时间。

    Returns:
        Optional[MirrorSource]: 最佳镜像源。
    """

    async def _check_single_mirror(mirror: MirrorSource) -> tuple[MirrorSource, float]:
        """
        检查单个镜像源的可用性。
        Args:
            mirror (MirrorSource): 镜像源。

        Returns:
            tuple[MirrorSource, float]: 镜像源和连接耗时。
        """
        try:
            parsed_url = urlparse(mirror.url)
            host = parsed_url.hostname
            port = parsed_url.port or (443 if parsed_url.scheme == "https" else 80)

            start_time = asyncio.get_event_loop().time()

            _, _ = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=timeout
            )

            elapsed = asyncio.get_event_loop().time() - start_time
            return mirror, elapsed

        except (asyncio.TimeoutError, ConnectionRefusedError, socket.gaierror) as e:
            logger.debug(f"镜像源 {mirror.name} 连接失败: {e!s}")
        return mirror, float("inf")

    tasks = [_check_single_mirror(mirror) for mirror in mirrors]
    results = await asyncio.gather(*tasks)

    available_mirrors = [(m, t) for m, t in results if t != float("inf")]
    if not available_mirrors:
        return None

    logger.debug(f"可用镜像源: {available_mirrors}")
    return min(available_mirrors, key=lambda x: (x[1], -x[0].priority))[0]


@asynccontextmanager
async def download_host_context(mirrors: list[MirrorSource]) -> AsyncIterator[None]:
    """
    为下载设置镜像源上下文管理器。
    Args:
        mirrors (list[MirrorSource]): 镜像源列表。

    Returns:
        AsyncIterator[None]: 上下文管理器。
    """
    had_original = "PLAYWRIGHT_DOWNLOAD_HOST" in os.environ
    original_host = os.environ.get("PLAYWRIGHT_DOWNLOAD_HOST")

    try:
        best_mirror = await check_mirror_connectivity(mirrors)

        if plugin_config.htmlrender_download_host:
            logger.info(f"使用配置的下载源: {plugin_config.htmlrender_download_host}")
            os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = (
                plugin_config.htmlrender_download_host
            )
        elif best_mirror:
            logger.info(f"使用镜像源: {best_mirror.name} ({best_mirror.url})")
            os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = best_mirror.url
        else:
            logger.info("无可用镜像源，使用默认源")

        yield
    finally:
        if had_original and original_host is not None:
            os.environ["PLAYWRIGHT_DOWNLOAD_HOST"] = original_host
        elif "PLAYWRIGHT_DOWNLOAD_HOST" in os.environ:
            del os.environ["PLAYWRIGHT_DOWNLOAD_HOST"]


class MessageType(Enum):
    PROGRESS = "progress"
    DOWNLOAD = "download"
    INFO = "info"
    ERROR = "error"


async def read_stream(stream, out: TextIO = sys.stdout) -> None:
    """实时读取并输出流内容

    Args:
        stream: 要读取的流
        out: 输出流，默认为 sys.stdout
    """
    last_progress = ""

    def write_progress(_: str) -> None:
        """写入进度条"""
        out.write(f"\r{_}")
        out.flush()

    def ensure_newline() -> None:
        """确保进度条后换行"""
        nonlocal last_progress
        if last_progress:
            out.write("\n")
            out.flush()
            last_progress = ""

    def get_message_type(_: str) -> MessageType:
        """获取消息类型"""
        if "|" in _ and "%" in _ and ("MiB" in _ or "KiB" in _):
            return MessageType.PROGRESS
        elif _.startswith("Downloading "):
            return MessageType.DOWNLOAD
        elif _.startswith("Error:"):
            return MessageType.ERROR
        return MessageType.INFO

    while True:
        line = await stream.readline()
        if not line:
            break

        text = line.decode().strip()
        if not text:
            continue

        msg_type = get_message_type(text)

        match msg_type:
            case MessageType.PROGRESS:
                progress_text = text.split("|", 1)[1].strip()
                write_progress(progress_text)
                last_progress = text
            case MessageType.ERROR:
                ensure_newline()
                raise PlaywrightInstallError(text)
            case _:
                ensure_newline()
                logger.info(text)


async def execute_install_command(
    install_cmd: list[str], timeout: int
) -> tuple[bool, str]:
    """
    执行安装命令并返回结果。
    Args:
        install_cmd (list[str]): 安装命令。
        timeout (int): 等待超时时间。

    Returns:
        tuple[bool, str]: 是否安装成功和消息。
    """
    process = await asyncio.create_subprocess_exec(
        *install_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        await asyncio.wait_for(
            asyncio.gather(
                read_stream(process.stdout),
                read_stream(process.stderr),
            ),
            timeout=timeout,
        )

        await process.wait()
        return (
            process.returncode == 0,
            "安装完成" if process.returncode == 0 else f"返回码 {process.returncode}",
        )
    except asyncio.TimeoutError:
        return False, "安装超时"
    except PlaywrightInstallError as e:
        return False, str(e)
    finally:
        if process and process.returncode is None:
            process.kill()
            await process.wait()


async def install_browser(
    browser_type: str = "chromium", timeout: int = 300, retries: int = 2
) -> bool:
    """
    安装用于 HTML 渲染的浏览器。

    Args:
        browser_type (str): 要安装的浏览器类型 ("chromium"、"firefox" 或 "webkit")。
        timeout (int): 安装过程中等待的最大秒数。
        retries (int): 安装失败时的最大重试次数。

    Returns:
        bool: 如果安装成功返回 True，否则返回 False
    """

    def _switch_to_official_mirror() -> None:
        """切换至官方源，移除自定义下载地址环境变量"""
        logger.info("切换至官方源重试...")
        if "PLAYWRIGHT_DOWNLOAD_HOST" in os.environ:
            del os.environ["PLAYWRIGHT_DOWNLOAD_HOST"]

    async with download_host_context(MIRRORS):
        install_cmd = ["playwright", "install", "--with-deps", browser_type]

        for attempt in range(1, retries + 1):
            try:
                logger.info(
                    f"正在安装 {browser_type}（第 {attempt}/{retries} 次尝试）..."
                )
                success, message = await execute_install_command(install_cmd, timeout)

                if success:
                    logger.success(f"{browser_type} 安装成功")
                    return True
                logger.error(f"安装失败：{message}")
                if "404" in message:
                    _switch_to_official_mirror()
                    continue

            except FileNotFoundError:
                logger.error(
                    "未找到 playwright 可执行文件，请确保已安装 playwright，"
                    "或正确进入虚拟环境"
                )
                return False

            except Exception as e:
                logger.error(f"安装过程中出现异常：{e!s}")

            if attempt < retries:
                await asyncio.sleep(2)

        logger.error(f"在 {retries} 次尝试后安装失败")
        return False
