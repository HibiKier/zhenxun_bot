import asyncio
import os
import base64
import re
import random


from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.image_utils import BuildImage
from utils.message_builder import image
from utils.browser import get_browser

def resize(path: str):
    """
    调整图像大小的异步函数

    Args:
        path (str): 图像文件路径
    """
    A = BuildImage(0, 0, background=path, ratio=0.5)
    A.save(path)

async def get_b64_image(url):
    """
    获取Bilibili链接的截图，并返回base64格式的图片

    Args:
        url (str): Bilibili链接

    Returns:
        image: base64格式的图片
    """
    cv_match = None
    opus_match = None
    t_opus_match = None

    cv_number = None
    opus_number = None
    t_opus_number = None

    # 提取cv、opus、t_opus的编号
    url = url.split("?")[0]
    cv_match = re.search(r'read/cv([A-Za-z0-9]+)', url, re.IGNORECASE)
    opus_match = re.search(r'opus/([A-Za-z0-9]+)', url, re.IGNORECASE)
    t_opus_match = re.search(r'https://t\.bilibili\.com/(\d+)', url, re.IGNORECASE)

    if cv_match:
        cv_number = cv_match.group(1)
    elif opus_match:
        opus_number = opus_match.group(1)
    elif t_opus_match:
        t_opus_number = t_opus_match.group(1)

    screenshot_path = None

    # 根据编号构建保存路径
    if cv_number:
        screenshot_path = f"{IMAGE_PATH}/bilibiliParse/cv_{cv_number}.png"
    elif opus_number:
        screenshot_path = f"{IMAGE_PATH}/bilibiliParse/opus_{opus_number}.png"
    elif t_opus_number:
        screenshot_path = f"{IMAGE_PATH}/bilibiliParse/opus_{t_opus_number}.png"
        # t.bilibili.com和https://www.bilibili.com/opus在内容上是一样的，为便于维护，调整url至https://www.bilibili.com/opus/
        url = f"https://www.bilibili.com/opus/{t_opus_number}"

    if screenshot_path:
        try:
            # 如果文件不存在，进行截图
            if not os.path.exists(screenshot_path):
                page = None
                browser = get_browser()
                if not browser:
                    return None
                
                # 创建页面
                user_agents = [
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
                    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
                ]
                # random.choice(),从列表中随机抽取一个对象
                user_agent = random.choice(user_agents) 
                try:
                    page = await browser.new_page(user_agent = user_agent)
                    await page.set_viewport_size({"width": 5120, "height": 2560})
                    # 设置请求拦截器
                    await page.route(re.compile(r"(\.png$)|(\.jpg$)"), lambda route: route.abort())
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
                    await div.screenshot(path=screenshot_path, timeout=100000, animations="disabled", type="png")
                    # 异步执行调整截图大小的操作
                    await asyncio.get_event_loop().run_in_executor(None, resize, screenshot_path)
                except Exception as e:
                    logger.warning(f"尝试解析bilibili转发失败 {type(e)}：{e}")
                    return None

                # 关闭页面
                if page:
                    await page.close()
                    if browser:
                        await browser.close()

            # 读取截图文件，转换为base64格式
            with open(screenshot_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                msg_image = image(f"base64://{base64_image}")

            return msg_image
        except Exception as e:
            logger.error(f"尝试解析bilibili转发失败 {type(e)}：{e}")
            return None
