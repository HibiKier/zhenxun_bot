from pathlib import Path

import nonebot
import pytest
from nonebot.plugin import Plugin
from nonebug import NONEBOT_INIT_KWARGS
from nonebug.app import App
from pytest_mock import MockerFixture
from respx import MockRouter


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi+~httpx+~websockets",
        "superusers": ["AkashiCoin"],
        "command_start": "",
        "session_running_expression": "别急呀,小真寻要宕机了!QAQ",
        "image_to_bytes": False,
        "nickname": ["真寻", "小真寻", "绪山真寻", "小寻子"],
        "session_expire_timeout": 30,
        "self_nickname": "小真寻",
        "db_url": "sqlite://:memory:",
        "platform_superusers": {"qq": ["qq_su"], "dodo": ["dodo_su"]},
        "host": "127.0.0.1",
        "port": 8080,
    }


@pytest.fixture(scope="session", autouse=True)
def load_plugin(nonebug_init: None) -> set[Plugin]:
    return nonebot.load_plugins("zhenxun.plugins")


@pytest.fixture
async def app(app: App, tmp_path: Path, mocker: MockerFixture):
    mocker.patch("nonebot.drivers.websockets.connect", return_value=MockRouter())
    return app
