import asyncio
from asyncio.exceptions import TimeoutError
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, Literal

import aiofiles
import httpx
import rich
from httpx import ConnectTimeout, Response
from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_htmlrender import get_browser
from playwright.async_api import Page
from retrying import retry

from zhenxun.configs.config import BotConfig
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.user_agent import get_user_agent

# from .browser import get_browser


class AsyncHttpx:

    proxy = {"http://": BotConfig.system_proxy, "https://": BotConfig.system_proxy}

    @classmethod
    @retry(stop_max_attempt_number=3)
    async def get(
        cls,
        url: str,
        *,
        params: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
        cookies: Dict[str, str] | None = None,
        verify: bool = True,
        use_proxy: bool = True,
        proxy: Dict[str, str] | None = None,
        timeout: int = 30,
        **kwargs,
    ) -> Response:
        """Get

        参数:
            url: url
            params: params
            headers: 请求头
            cookies: cookies
            verify: verify
            use_proxy: 使用默认代理
            proxy: 指定代理
            timeout: 超时时间
        """
        if not headers:
            headers = get_user_agent()
        _proxy = proxy if proxy else cls.proxy if use_proxy else None
        async with httpx.AsyncClient(proxies=_proxy, verify=verify) as client:  # type: ignore
            return await client.get(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                **kwargs,
            )

    @classmethod
    async def post(
        cls,
        url: str,
        *,
        data: Dict[str, Any] | None = None,
        content: Any = None,
        files: Any = None,
        verify: bool = True,
        use_proxy: bool = True,
        proxy: Dict[str, str] | None = None,
        json: Dict[str, Any] | None = None,
        params: Dict[str, str] | None = None,
        headers: Dict[str, str] | None = None,
        cookies: Dict[str, str] | None = None,
        timeout: int = 30,
        **kwargs,
    ) -> Response:
        """
        说明:
            Post
        参数:
            url: url
            data: data
            content: content
            files: files
            use_proxy: 是否默认代理
            proxy: 指定代理
            json: json
            params: params
            headers: 请求头
            cookies: cookies
            timeout: 超时时间
        """
        if not headers:
            headers = get_user_agent()
        _proxy = proxy if proxy else cls.proxy if use_proxy else None
        async with httpx.AsyncClient(proxies=_proxy, verify=verify) as client:  # type: ignore
            return await client.post(
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                **kwargs,
            )

    @classmethod
    async def download_file(
        cls,
        url: str,
        path: str | Path,
        *,
        params: Dict[str, str] | None = None,
        verify: bool = True,
        use_proxy: bool = True,
        proxy: Dict[str, str] | None = None,
        headers: Dict[str, str] | None = None,
        cookies: Dict[str, str] | None = None,
        timeout: int = 30,
        stream: bool = False,
        **kwargs,
    ) -> bool:
        """下载文件

        参数:
            url: url
            path: 存储路径
            params: params
            verify: verify
            use_proxy: 使用代理
            proxy: 指定代理
            headers: 请求头
            cookies: cookies
            timeout: 超时时间
            stream: 是否使用流式下载（流式写入+进度条，适用于下载大文件）
        """
        if isinstance(path, str):
            path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            for _ in range(3):
                if not stream:
                    try:
                        content = (
                            await cls.get(
                                url,
                                params=params,
                                headers=headers,
                                cookies=cookies,
                                use_proxy=use_proxy,
                                proxy=proxy,
                                timeout=timeout,
                                **kwargs,
                            )
                        ).content
                        async with aiofiles.open(path, "wb") as wf:
                            await wf.write(content)
                            logger.info(f"下载 {url} 成功.. Path：{path.absolute()}")
                        return True
                    except (TimeoutError, ConnectTimeout):
                        pass
                else:
                    if not headers:
                        headers = get_user_agent()
                    _proxy = proxy if proxy else cls.proxy if use_proxy else None
                    try:
                        async with httpx.AsyncClient(
                            proxies=_proxy, verify=verify  # type: ignore
                        ) as client:
                            async with client.stream(
                                "GET",
                                url,
                                params=params,
                                headers=headers,
                                cookies=cookies,
                                timeout=timeout,
                                **kwargs,
                            ) as response:
                                logger.info(
                                    f"开始下载 {path.name}.. Path: {path.absolute()}"
                                )
                                async with aiofiles.open(path, "wb") as wf:
                                    total = int(response.headers["Content-Length"])
                                    with rich.progress.Progress(  # type: ignore
                                        rich.progress.TextColumn(path.name),  # type: ignore
                                        "[progress.percentage]{task.percentage:>3.0f}%",  # type: ignore
                                        rich.progress.BarColumn(bar_width=None),  # type: ignore
                                        rich.progress.DownloadColumn(),  # type: ignore
                                        rich.progress.TransferSpeedColumn(),  # type: ignore
                                    ) as progress:
                                        download_task = progress.add_task(
                                            "Download", total=total
                                        )
                                        async for chunk in response.aiter_bytes():
                                            await wf.write(chunk)
                                            await wf.flush()
                                            progress.update(
                                                download_task,
                                                completed=response.num_bytes_downloaded,
                                            )
                                    logger.info(
                                        f"下载 {url} 成功.. Path：{path.absolute()}"
                                    )
                        return True
                    except (TimeoutError, ConnectTimeout):
                        pass
            else:
                logger.error(f"下载 {url} 下载超时.. Path：{path.absolute()}")
        except Exception as e:
            logger.error(f"下载 {url} 错误 Path：{path.absolute()}", e=e)
        return False

    @classmethod
    async def gather_download_file(
        cls,
        url_list: list[str],
        path_list: list[str | Path],
        *,
        limit_async_number: int | None = None,
        params: Dict[str, str] | None = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] | None = None,
        headers: Dict[str, str] | None = None,
        cookies: Dict[str, str] | None = None,
        timeout: int = 30,
        **kwargs,
    ) -> list[bool]:
        """分组同时下载文件

        参数:
            url_list: url列表
            path_list: 存储路径列表
            limit_async_number: 限制同时请求数量
            params: params
            use_proxy: 使用代理
            proxy: 指定代理
            headers: 请求头
            cookies: cookies
            timeout: 超时时间
        """
        if n := len(url_list) != len(path_list):
            raise UrlPathNumberNotEqual(
                f"Url数量与Path数量不对等，Url：{len(url_list)}，Path：{len(path_list)}"
            )
        if limit_async_number and n > limit_async_number:
            m = float(n) / limit_async_number
            x = 0
            j = limit_async_number
            _split_url_list = []
            _split_path_list = []
            for _ in range(int(m)):
                _split_url_list.append(url_list[x:j])
                _split_path_list.append(path_list[x:j])
                x += limit_async_number
                j += limit_async_number
            if int(m) < m:
                _split_url_list.append(url_list[j:])
                _split_path_list.append(path_list[j:])
        else:
            _split_url_list = [url_list]
            _split_path_list = [path_list]
        tasks = []
        result_ = []
        for x, y in zip(_split_url_list, _split_path_list):
            for url, path in zip(x, y):
                tasks.append(
                    asyncio.create_task(
                        cls.download_file(
                            url,
                            path,
                            params=params,
                            headers=headers,
                            cookies=cookies,
                            use_proxy=use_proxy,
                            timeout=timeout,
                            proxy=proxy,
                            **kwargs,
                        )
                    )
                )
            _x = await asyncio.gather(*tasks)
            result_ = result_ + list(_x)
            tasks.clear()
        return result_


class AsyncPlaywright:
    @classmethod
    @asynccontextmanager
    async def new_page(cls, **kwargs) -> AsyncGenerator[Page, None]:
        """获取一个新页面

        参数:
            user_agent: 请求头
        """
        browser = await get_browser()
        ctx = await browser.new_context(**kwargs)
        page = await ctx.new_page()
        try:
            yield page
        finally:
            await page.close()
            await ctx.close()

    @classmethod
    async def screenshot(
        cls,
        url: str,
        path: Path | str,
        element: str | list[str],
        *,
        wait_time: int | None = None,
        viewport_size: Dict[str, int] | None = None,
        wait_until: (
            Literal["domcontentloaded", "load", "networkidle"] | None
        ) = "networkidle",
        timeout: float | None = None,
        type_: Literal["jpeg", "png"] | None = None,
        user_agent: str | None = None,
        **kwargs,
    ) -> UniMessage | None:
        """截图，该方法仅用于简单快捷截图，复杂截图请操作 page

        参数:
            url: 网址
            path: 存储路径
            element: 元素选择
            wait_time: 等待截取超时时间
            viewport_size: 窗口大小
            wait_until: 等待类型
            timeout: 超时限制
            type_: 保存类型
        """
        if viewport_size is None:
            viewport_size = dict(width=2560, height=1080)
        if isinstance(path, str):
            path = Path(path)
        wait_time = wait_time * 1000 if wait_time else None
        if isinstance(element, str):
            element_list = [element]
        else:
            element_list = element
        async with cls.new_page(
            viewport=viewport_size,
            user_agent=user_agent,
            **kwargs,
        ) as page:
            await page.goto(url, timeout=timeout, wait_until=wait_until)
            card = page
            for e in element_list:
                if not card:
                    return None
                card = await card.wait_for_selector(e, timeout=wait_time)
            if card:
                await card.screenshot(path=path, timeout=timeout, type=type_)
                return MessageUtils.build_message(path)
        return None


class UrlPathNumberNotEqual(Exception):
    pass


class BrowserIsNone(Exception):
    pass
