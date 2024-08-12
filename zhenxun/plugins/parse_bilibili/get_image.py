import os
import re
from pathlib import Path

from nonebot_plugin_alconna import UniMessage

from zhenxun.configs.path_config import TEMP_PATH
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncPlaywright
from zhenxun.utils.image_utils import BuildImage
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.user_agent import get_user_agent_str


async def resize(path: Path):
    """调整图像大小的异步函数

    参数:
        path (str): 图像文件路径
    """
    A = BuildImage.open(path)
    await A.resize(0.8)
    await A.save(path)


async def get_image(url) -> UniMessage | None:
    """获取Bilibili链接的截图，并返回base64格式的图片

    参数:
        url (str): Bilibili链接

    返回:
        Image: Image
    """
    cv_match = None
    opus_match = None
    t_opus_match = None

    cv_number = None
    opus_number = None
    t_opus_number = None

    # 提取cv、opus、t_opus的编号
    url = url.split("?")[0]
    cv_match = re.search(r"read/cv([A-Za-z0-9]+)", url, re.IGNORECASE)
    opus_match = re.search(r"opus/([A-Za-z0-9]+)", url, re.IGNORECASE)
    t_opus_match = re.search(r"https://t\.bilibili\.com/(\d+)", url, re.IGNORECASE)

    if cv_match:
        cv_number = cv_match.group(1)
    elif opus_match:
        opus_number = opus_match.group(1)
    elif t_opus_match:
        t_opus_number = t_opus_match.group(1)

    screenshot_path = None

    # 根据编号构建保存路径
    if cv_number:
        screenshot_path = TEMP_PATH / "bilibili_cv_{cv_number}.png"
    elif opus_number:
        screenshot_path = TEMP_PATH / "bilibili_opus_{opus_number}.png"
    elif t_opus_number:
        screenshot_path = TEMP_PATH / "bilibili_opus_{t_opus_number}.png"
        # t.bilibili.com和https://www.bilibili.com/opus在内容上是一样的，为便于维护，调整url至https://www.bilibili.com/opus/
        url = f"https://www.bilibili.com/opus/{t_opus_number}"
    if screenshot_path:
        try:
            # 如果文件不存在，进行截图
            if not screenshot_path.exists():
                # 创建页面
                try:
                    async with AsyncPlaywright.new_page() as page:
                        await page.set_viewport_size({"width": 5120, "height": 2560})
                        # 设置请求拦截器
                        await page.route(
                            re.compile(r"(\.png$)|(\.jpg$)"),
                            lambda route: route.abort(),
                        )
                        # 访问链接
                        await page.goto(url, wait_until="networkidle", timeout=10000)
                        # 根据不同的链接结构，设置对应的CSS选择器
                        if cv_number:
                            css = "#app > div"
                        elif opus_number or t_opus_number:
                            css = "#app > div.opus-detail > div.bili-opus-view"
                        # 点击对应的元素
                        await page.click(css)
                        # 查询目标元素
                        div = await page.query_selector(css)
                        # 对目标元素进行截图
                        await div.screenshot(  # type: ignore
                            path=screenshot_path,
                            timeout=100000,
                            animations="disabled",
                            type="png",
                        )
                        # 异步执行调整截图大小的操作
                        await resize(screenshot_path)
                except Exception as e:
                    logger.warning(f"尝试解析bilibili转发失败", e=e)
                    return None
            return MessageUtils.build_message(screenshot_path)
        except Exception as e:
            logger.error(f"尝试解析bilibili转发失败", e=e)
        return None
