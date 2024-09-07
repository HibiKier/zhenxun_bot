import platform
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

platform_uname = platform.uname_result(
    system="Linux",
    node="zhenxun",
    release="5.15.0-1027-azure",
    version="#1 SMP Debian 5.15.0-1027-azure",
    machine="x86_64",
)  # type: ignore
cpuinfo_get_cpu_info = {"brand_raw": "Intel(R) Core(TM) i7-10700K"}


def init_mocker(mocker: MockerFixture, tmp_path: Path):
    mock_psutil = mocker.patch("zhenxun.builtin_plugins.check.data_source.psutil")
    mock_cpuinfo = mocker.patch("zhenxun.builtin_plugins.check.data_source.cpuinfo")
    mock_cpuinfo.get_cpu_info.return_value = cpuinfo_get_cpu_info

    mock_platform = mocker.patch("zhenxun.builtin_plugins.check.data_source.platform")
    mock_platform.uname.return_value = platform_uname

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
    return (
        mock_psutil,
        mock_cpuinfo,
        mock_platform,
        mock_template_to_pic,
        mock_template_to_pic_return,
        mock_build_message,
        mock_build_message_return,
        mock_template_path_new,
    )


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

    (
        mock_psutil,
        mock_cpuinfo,
        mock_platform,
        mock_template_to_pic,
        mock_template_to_pic_return,
        mock_build_message,
        mock_build_message_return,
        mock_template_path_new,
    ) = init_mocker(mocker, tmp_path)
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
                "brand_raw": cpuinfo_get_cpu_info["brand_raw"],
                "baidu": "red",
                "google": "red",
                "system": f"{platform_uname.system} " f"{platform_uname.release}",
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
    mock_template_to_pic.assert_awaited_once()
    mock_build_message.assert_called_once_with(mock_template_to_pic_return)
    mock_build_message_return.send.assert_awaited_once()


async def test_check_arm(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试自检（arm）
    """
    from zhenxun.configs.config import BotConfig
    from zhenxun.builtin_plugins.check import _matcher
    from zhenxun.builtin_plugins.check.data_source import __get_version

    platform_uname_arm = platform.uname_result(
        system="Linux",
        node="zhenxun",
        release="5.15.0-1017-oracle",
        version="#22~20.04.1-Ubuntu SMP Wed Aug 24 11:13:15 UTC 2022",
        machine="aarch64",
    )  # type: ignore
    mock_subprocess_check_output = mocker.patch(
        "zhenxun.builtin_plugins.check.data_source.subprocess.check_output"
    )
    mock_environ_copy = mocker.patch(
        "zhenxun.builtin_plugins.check.data_source.os.environ.copy"
    )
    mock_environ_copy_return = mocker.MagicMock()
    mock_environ_copy.return_value = mock_environ_copy_return
    (
        mock_psutil,
        mock_cpuinfo,
        mock_platform,
        mock_template_to_pic,
        mock_template_to_pic_return,
        mock_build_message,
        mock_build_message_return,
        mock_template_path_new,
    ) = init_mocker(mocker, tmp_path)

    mock_platform.uname.return_value = platform_uname_arm
    mock_cpuinfo.get_cpu_info.return_value = {}
    mock_psutil.cpu_freq.return_value = {}

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
                "cpu_info": "1.0% - 0.0Ghz [1 core]",
                "cpu_process": 1.0,
                "ram_info": "1.0 / 1.0 GB",
                "ram_process": 100.0,
                "swap_info": "1.0 / 1.0 GB",
                "swap_process": 100.0,
                "disk_info": "1.0 / 1.0 GB",
                "disk_process": 100.0,
                "brand_raw": "",
                "baidu": "red",
                "google": "red",
                "system": f"{platform_uname_arm.system} "
                f"{platform_uname_arm.release}",
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
    mock_subprocess_check_output.assert_has_calls(
        [
            mocker.call(["lscpu"], env=mock_environ_copy_return),
            mocker.call().decode(),
            mocker.call().decode().splitlines(),
            mocker.call().decode().splitlines().__iter__(),
            mocker.call(["dmidecode", "-s", "processor-frequency"]),
            mocker.call().decode(),
            mocker.call().decode().split(),
            mocker.call().decode().split().__getitem__(0),
            mocker.call().decode().split().__getitem__().__float__(),
        ]  # type: ignore
    )
    mock_template_to_pic.assert_awaited_once()
    mock_build_message.assert_called_once_with(mock_template_to_pic_return)
    mock_build_message_return.send.assert_awaited_once()
