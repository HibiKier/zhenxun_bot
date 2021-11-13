from configs.path_config import IMAGE_PATH
from utils.image_utils import CreateImg
from utils.message_builder import image
from services.log import logger
from utils.browser import get_browser
from playwright._impl._api_types import TimeoutError

csgola_url = "https://www.csgola.com/player/"
_5e_url = "https://arena.5eplay.com/data/player/"


async def get_csgola_data(uid: int) -> "str, int":
    page = None
    try:
        browser = await get_browser()
        if not browser:
            return "", 997
        page = await browser.new_page()
        for _ in range(3):
            try:
                await page.goto(f"{csgola_url}{uid}", wait_until="networkidle", timeout=10000)
                break
            except TimeoutError:
                pass
        else:
            return '连接超时...', 995
        await page.set_viewport_size({"width": 2560, "height": 1080})

        data = await page.query_selector_all(".panel-body")
        if not data:
            return "未查询到该Id....", 999
        await data[0].screenshot(path=f"{IMAGE_PATH}/temp/{uid}_1.png", timeout=100000)
        await data[3].screenshot(path=f"{IMAGE_PATH}/temp/{uid}_2.png", timeout=100000)
        await data[5].screenshot(path=f"{IMAGE_PATH}/temp/{uid}_3.png", timeout=100000)
        await data[7].screenshot(path=f"{IMAGE_PATH}/temp/{uid}_5.png", timeout=100000)

        ava = await page.query_selector("div.container:nth-child(4) > div:nth-child(1)")
        await ava.screenshot(path=f"{IMAGE_PATH}/temp/{uid}_0.png", timeout=100000)

        weapon_data = await page.query_selector(".gun-stats-sec")
        await weapon_data.screenshot(
            path=f"{IMAGE_PATH}/temp/{uid}_4.png", timeout=100000
        )

        ava = CreateImg(0, 0, background=f"{IMAGE_PATH}/temp/{uid}_0.png")
        statistical_data = CreateImg(0, 0, background=f"{IMAGE_PATH}/temp/{uid}_1.png")
        combined_data = CreateImg(0, 0, background=f"{IMAGE_PATH}/temp/{uid}_2.png")
        detailed_data = CreateImg(0, 0, background=f"{IMAGE_PATH}/temp/{uid}_3.png")
        weapon_data = CreateImg(0, 0, background=f"{IMAGE_PATH}/temp/{uid}_4.png")
        map_data = CreateImg(0, 0, background=f"{IMAGE_PATH}/temp/{uid}_5.png")
        if statistical_data.h > 300:
            statistical_data.crop((0, 0, statistical_data.w, 300))
        if combined_data.h > 260:
            combined_data.crop((0, 0, combined_data.w, 260))
        if detailed_data.h > 400:
            detailed_data.crop((0, 0, detailed_data.w, 400))
        weapon_data.crop((0, 100, weapon_data.w, weapon_data.h))
        map_data.crop((0, 310, map_data.w, map_data.h))
        height = (
            ava.h
            + statistical_data.h
            + combined_data.h
            + detailed_data.h
            + weapon_data.h
            + map_data.h
        )
        bk = CreateImg(1168, height)
        current_h = 0
        for img in [
            ava,
            statistical_data,
            combined_data,
            detailed_data,
            weapon_data,
            map_data,
        ]:
            bk.paste(img, (0, current_h))
            current_h += img.h
        bk.save(f"{IMAGE_PATH}/temp/csgo_{uid}.png")
    except Exception as e:
        logger.error(f"生成csgola图片错误 {type(e)}：{e}")
        if page:
            await page.close()
        return "发生了错误....", 998
    if page:
        await page.close()
    return image(f"csgo_{uid}.png", "temp"), 200


async def get_5e_data(uname: str) -> "str, int":
    page = None
    try:
        browser = await get_browser()
        if not browser:
            return "", 997
        page = await browser.new_page()
        await page.goto(f"{_5e_url}{uname}", wait_until="networkidle", timeout=10000)
        if "HTTP ERROR 404" in await page.content():
            return "未查询到该玩家...", 999
        await page.set_viewport_size({"width": 2560, "height": 1080})
        body = await page.query_selector("body")
        await body.screenshot(
            path=f"{IMAGE_PATH}/temp/csgo_{uname}_0.png", timeout=100000
        )
        await page.click("a.match-tab-item:nth-child(2)")
        body = await page.query_selector("body")
        await body.screenshot(
            path=f"{IMAGE_PATH}/temp/csgo_{uname}_1.png", timeout=100000
        )
        await page.click("a.match-tab-item:nth-child(1)")
        body = await page.query_selector("body")
        await body.screenshot(
            path=f"{IMAGE_PATH}/temp/csgo_{uname}_2.png", timeout=100000
        )
        bk = CreateImg(1344 * 3, 2307)
        current_w = 0
        for i in range(3):
            body = CreateImg(0, 0, background=f"{IMAGE_PATH}/temp/csgo_{uname}_{i}.png")
            body.crop((600, 90, body.w - 600, body.h - 410))
            bk.paste(body, (current_w, 0))
            current_w += 1344
        bk.save(f"{IMAGE_PATH}/temp/csgo_{uname}.png")
    except Exception as e:
        logger.error(f"生成5e图片错误 {type(e)}：{e}")
        if page:
            await page.close()
            return "发生了错误...", 998
    if page:
        await page.close()
    return image(f"csgo_{uname}.png", "temp"), 200
