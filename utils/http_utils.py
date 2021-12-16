from typing import Dict, Union, Optional, List, Any, Literal
from utils.user_agent import get_user_agent
from .utils import get_local_proxy
from services.log import logger
from pathlib import Path
from httpx import Response
from asyncio.exceptions import TimeoutError
from nonebot.adapters.cqhttp import MessageSegment
from playwright.async_api import Page
from .message_builder import image
from httpx import ConnectTimeout
from .browser import get_browser
from retrying import retry
import asyncio
import aiofiles
import httpx


class AsyncHttpx:

    proxy = {"http://": get_local_proxy(), "https://": get_local_proxy()}

    @classmethod
    @retry(stop_max_attempt_number=3)
    async def get(
        cls,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        allow_redirects: bool = True,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> Response:
        """
        说明：
            Get
        参数：
            :param url: url
            :param params: params
            :param headers: 请求头
            :param cookies: cookies
            :param use_proxy: 使用默认代理
            :param proxy: 指定代理
            :param allow_redirects: allow_redirects
            :param timeout: 超时时间
        """
        if not headers:
            headers = get_user_agent()
        proxy = proxy if proxy else cls.proxy if use_proxy else None
        async with httpx.AsyncClient(proxies=proxy) as client:
            return await client.get(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                allow_redirects=allow_redirects,
                timeout=timeout,
                **kwargs
            )

    @classmethod
    async def post(
        cls,
        url: str,
        *,
        data: Optional[Dict[str, str]] = None,
        content: Any = None,
        files: Any = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        json: Optional[Dict[str, Union[Any]]] = None,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        allow_redirects: bool = True,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> Response:
        """
        说明：
            Post
        参数：
            :param url: url
            :param data: data
            :param content: content
            :param files: files
            :param use_proxy: 是否默认代理
            :param proxy: 指定代理
            :param json: json
            :param params: params
            :param headers: 请求头
            :param cookies: cookies
            :param allow_redirects: allow_redirects
            :param timeout: 超时时间
        """
        if not headers:
            headers = get_user_agent()
        proxy = proxy if proxy else cls.proxy if use_proxy else None
        async with httpx.AsyncClient(proxies=proxy) as client:
            return await client.post(
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                allow_redirects=allow_redirects,
                timeout=timeout,
                **kwargs,
            )

    @classmethod
    async def download_file(
        cls,
        url: str,
        path: Union[str, Path],
        *,
        params: Optional[Dict[str, str]] = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> bool:
        """
        说明：
            下载文件
        参数：
            :param url: url
            :param path: 存储路径
            :param params: params
            :param use_proxy: 使用代理
            :param proxy: 指定代理
            :param headers: 请求头
            :param cookies: cookies
            :param timeout: 超时时间
        """
        if isinstance(path, str):
            path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            for _ in range(3):
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
                logger.error(f"下载 {url} 下载超时.. Path：{path.absolute()}")
        except Exception as e:
            logger.error(f"下载 {url} 未知错误 {type(e)}：{e}.. Path：{path.absolute()}")
        return False

    @classmethod
    async def gather_download_file(
        cls,
        url_list: List[str],
        path_list: List[Union[str, Path]],
        *,
        limit_async_number: Optional[int] = None,
        params: Optional[Dict[str, str]] = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> List[bool]:
        """
        说明：
            分组同时下载文件
        参数：
            :param url_list: url列表
            :param path_list: 存储路径列表
            :param limit_async_number: 限制同时请求数量
            :param params: params
            :param use_proxy: 使用代理
            :param proxy: 指定代理
            :param headers: 请求头
            :param cookies: cookies
            :param timeout: 超时时间
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
                            ** kwargs,
                        )
                    )
                )
            _x = await asyncio.gather(*tasks)
            result_ = result_ + list(_x)
            tasks.clear()
        return result_


class AsyncPlaywright:

    @classmethod
    async def _new_page(cls, user_agent: Optional[str] = None, **kwargs) -> Page:
        """
        说明：
            获取一个新页面
        参数：
            :param user_agent: 请求头
        """
        browser = await get_browser()
        if browser:
            return await browser.new_page(user_agent=user_agent, **kwargs)
        raise BrowserIsNone("获取Browser失败...")

    @classmethod
    async def goto(
        cls,
        url: str,
        *,
        timeout: Optional[float] = 100000,
        wait_until: Optional[
            Literal["domcontentloaded", "load", "networkidle"]
        ] = "networkidle",
        referer: str = None,
        **kwargs
    ) -> Optional[Page]:
        """
        说明：
            goto
        参数：
            :param url: 网址
            :param timeout: 超时限制
            :param wait_until: 等待类型
            :param referer:
        """
        page = None
        try:
            page = await cls._new_page(**kwargs)
            await page.goto(url, timeout=timeout, wait_until=wait_until, referer=referer)
            return page
        except Exception as e:
            logger.warning(f"Playwright 访问 url：{url} 发生错误 {type(e)}：{e}")
            if page:
                await page.close()
        return None

    @classmethod
    async def screenshot(
        cls,
        url: str,
        path: Union[Path, str],
        element: str,
        *,
        sleep: Optional[int] = None,
        viewport_size: Dict[str, int] = None,
        wait_until: Optional[
            Literal["domcontentloaded", "load", "networkidle"]
        ] = "networkidle",
        timeout: float = None,
        type_: Literal["jpeg", "png"] = None,
        **kwargs
    ) -> Optional[MessageSegment]:
        """
        说明：
            截图，该方法仅用于简单快捷截图，复杂截图请操作 page
        参数：
            :param url: 网址
            :param path: 存储路径
            :param element: 元素选择
            :param sleep: 延迟截取
            :param viewport_size: 窗口大小
            :param wait_until: 等待类型
            :param timeout: 超时限制
            :param type_: 保存类型
        """
        page = None
        if viewport_size is None:
            viewport_size = dict(width=2560, height=1080)
        if isinstance(path, str):
            path = Path(path)
        try:
            page = await cls.goto(url, wait_until=wait_until, **kwargs)
            await page.set_viewport_size(viewport_size)
            if sleep:
                await asyncio.sleep(sleep)
            card = await page.query_selector(element)
            await card.screenshot(path=path, timeout=timeout, type=type_)
            return image(path)
        except Exception as e:
            logger.warning(f"Playwright 截图 url：{url} element：{element} 发生错误 {type(e)}：{e}")
        finally:
            if page:
                await page.close()
        return None


class UrlPathNumberNotEqual(Exception):
    pass


class BrowserIsNone(Exception):
    pass
