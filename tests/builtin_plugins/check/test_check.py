from typing import cast
from pathlib import Path
from collections.abc import Callable

import nonebot
from nonebug import App
from respx import MockRouter
from pytest_mock import MockerFixture
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent

from tests.utils import _v11_group_message_event
from tests.config import BotId, UserId, GroupId, MessageId


async def test_check(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试自检
    """
    from zhenxun.configs.config import BotConfig
    from zhenxun.builtin_plugins.check import _matcher
    from zhenxun.builtin_plugins.check.data_source import __get_version

    mocker.patch("zhenxun.builtin_plugins.check.data_source.psutil")
    mock_cpuinfo = mocker.patch("zhenxun.builtin_plugins.check.data_source.cpuinfo")
    mock_platform = mocker.patch("zhenxun.builtin_plugins.check.data_source.platform")

    mock_template_to_pic = mocker.patch("zhenxun.builtin_plugins.check.template_to_pic")
    mock_template_to_pic_return = mocker.AsyncMock()
    mock_template_to_pic.return_value = mock_template_to_pic_return

    mock_build_message = mocker.patch(
        "zhenxun.builtin_plugins.check.MessageUtils.build_message"
    )
    mock_build_message_return = mocker.AsyncMock()
    mock_build_message.return_value = mock_build_message_return

    mock_template_path_new = tmp_path / "resources" / "template"
    mocker.patch(
        "zhenxun.builtin_plugins.check.TEMPLATE_PATH", new=mock_template_path_new
    )

    async with app.test_matcher(_matcher) as ctx:
        bot = create_bot(ctx)
        bot: Bot = cast(Bot, bot)
        raw_message = "自检"
        event: GroupMessageEvent = _v11_group_message_event(
            message=raw_message,
            self_id=BotId.QQ_BOT,
            user_id=UserId.SUPERUSER,
            group_id=GroupId.GROUP_ID_LEVEL_5,
            message_id=MessageId.MESSAGE_ID_3,
            to_me=True,
        )
        ctx.receive_event(bot=bot, event=event)
    mock_template_to_pic.assert_awaited_once_with(
        template_path=str((mock_template_path_new / "check").absolute()),
        template_name="main.html",
        templates={
            "data": {
                "cpu_info": "1.0% - 1.0Ghz [1 core]",
                "cpu_process": 1.0,
                "ram_info": "1.0 / 1.0 GB",
                "ram_process": 100.0,
                "swap_info": "1.0 / 1.0 GB",
                "swap_process": 100.0,
                "disk_info": "1.0 / 1.0 GB",
                "disk_process": 100.0,
                "brand_raw": mock_cpuinfo.get_cpu_info().get(),
                "baidu": "red",
                "google": "red",
                "system": f"{mock_platform.uname().system} "
                f"{mock_platform.uname().release}",
                "version": __get_version(),
                "plugin_count": len(nonebot.get_loaded_plugins()),
                "nickname": BotConfig.self_nickname,
            }
        },
        pages={
            "viewport": {"width": 195, "height": 750},
            "base_url": f"file://{mock_template_path_new.absolute()}",
        },
        wait=2,
    )
    mock_build_message.assert_called_once_with(mock_template_to_pic_return)
    mock_build_message_return.send.assert_awaited_once()
