from collections.abc import AsyncGenerator
import pytest

from io import BytesIO
from nonebug import App
from PIL import Image, ImageChops

from .utils import count_to_color


@pytest.mark.asyncio
async def test_text_to_pic(app: App, load_playwright: AsyncGenerator):
    from zhenxun.builtin_plugins.htmlrender import text_to_pic

    async with app.test_server():
        img = await text_to_pic("114514")
        assert isinstance(img, bytes)


@pytest.mark.asyncio
async def test_md_to_pic(app: App, load_playwright: AsyncGenerator):
    from zhenxun.builtin_plugins.htmlrender import md_to_pic

    async with app.test_server():
        img = await md_to_pic("$$114514$$")
        assert isinstance(img, bytes)


@pytest.mark.asyncio
async def test_html_to_pic(app: App, load_playwright: AsyncGenerator):
    from zhenxun.builtin_plugins.htmlrender import html_to_pic

    async with app.test_server():
        img = await html_to_pic("<html><body><p>114514</p></body></html>")
        assert isinstance(img, bytes)


@pytest.mark.asyncio
async def test_template_to_pic(app: App, load_playwright: AsyncGenerator):
    from zhenxun.builtin_plugins.htmlrender import template_to_pic

    from pathlib import Path

    text_list = ["1", "2", "3", "4"]
    template_path = str(Path(__file__).parent / "templates")
    template_name = "text.html"

    async with app.test_server():
        img = await template_to_pic(
            template_path=template_path,
            template_name=template_name,
            templates={"text_list": text_list},
            pages={
                "viewport": {"width": 600, "height": 300},
                "base_url": f"file://{template_path}",
            },
            wait=2,
        )
        assert isinstance(img, bytes)


@pytest.mark.asyncio
async def test_template_filter(app: App, load_playwright: AsyncGenerator):
    from pathlib import Path
    from zhenxun.builtin_plugins.htmlrender import template_to_pic

    count_list = ["1", "2", "3", "4"]
    template_path = str(Path(__file__).parent / "templates")
    template_name = "progress.html.jinja2"

    async with app.test_server():
        image_byte = await template_to_pic(
            template_path=template_path,
            template_name=template_name,
            templates={"counts": count_list},
            filters={"count_to_color": count_to_color},
            pages={
                "viewport": {"width": 600, "height": 300},
                "base_url": f"file://{template_path}",
            },
        )

        test_image_path = Path(__file__).parent / "test_template_filter.png"
        test_image = Image.open(test_image_path)
        image = Image.open(BytesIO(initial_bytes=image_byte))
        diff = ImageChops.difference(image, test_image)
        assert diff.getbbox() is None
