from typing import cast
from pathlib import Path
from collections.abc import Callable

from nonebug import App
from respx import MockRouter
from pytest_mock import MockerFixture
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent

from tests.config import BotId, UserId, GroupId, MessageId
from tests.utils import get_response_json, _v11_group_message_event


def init_mocked_api(mocked_api: MockRouter) -> None:
    mocked_api.get(
        "https://cdn.jsdelivr.net/gh/zhenxun-org/zhenxun_bot_plugins/plugins.json",
        name="basic_plugins",
    ).respond(200, json=get_response_json("basic_plugins.json"))
    mocked_api.get(
        "https://raw.githubusercontent.com/zhenxun-org/zhenxun_bot_plugins_index/index/plugins.json",
        name="extra_plugins",
    ).respond(200, json=get_response_json("extra_plugins.json"))
    mocked_api.get(
        "https://api.github.com/repos/zhenxun-org/zhenxun_bot_plugins/contents/plugins/search_image?ref=main",
        name="search_image_plugin_api",
    ).respond(200, json=get_response_json("search_image_plugin_api.json"))
    mocked_api.get(
        "https://raw.githubusercontent.com/zhenxun-org/zhenxun_bot_plugins/main/plugins/search_image/__init__.py",
        name="search_image_plugin_file_init",
    ).respond(content=b"")
    mocked_api.get(
        "https://api.github.com/repos/xuanerwa/zhenxun_github_sub/contents/",
        name="github_sub_plugin_contents",
    ).respond(json=get_response_json("github_sub_plugin_contents.json"))
    mocked_api.get(
        "https://api.github.com/repos/xuanerwa/zhenxun_github_sub/contents/github_sub?ref=main",
        name="github_sub_plugin_api",
    ).respond(json=get_response_json("github_sub_plugin_api.json"))
    mocked_api.get(
        "https://raw.githubusercontent.com/xuanerwa/zhenxun_github_sub/main/github_sub/__init__.py",
        name="github_sub_plugin_file_init",
    ).respond(content=b"")


async def test_add_plugin_basic(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试添加基础插件
    """
    from zhenxun.builtin_plugins.plugin_store import _matcher

    init_mocked_api(mocked_api=mocked_api)
    mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        return_value=tmp_path / "zhenxun",
    )

    plugin_id = 1

    async with app.test_matcher(_matcher) as ctx:
        bot = create_bot(ctx)
        bot: Bot = cast(Bot, bot)
        raw_message = f"添加插件 {plugin_id}"
        event: GroupMessageEvent = _v11_group_message_event(
            message=raw_message,
            self_id=BotId.QQ_BOT,
            user_id=UserId.SUPERUSER,
            group_id=GroupId.GROUP_ID_LEVEL_5,
            message_id=MessageId.MESSAGE_ID,
            to_me=True,
        )
        ctx.receive_event(bot=bot, event=event)
        ctx.should_call_send(
            event=event,
            message=Message(message=f"正在添加插件 Id: {plugin_id}"),
            result=None,
            bot=bot,
        )
        ctx.should_call_send(
            event=event,
            message=Message(message="插件 识图 安装成功! 重启后生效"),
            result=None,
            bot=bot,
        )
    assert mocked_api["basic_plugins"].called
    assert mocked_api["extra_plugins"].called
    assert mocked_api["search_image_plugin_api"].called
    assert mocked_api["search_image_plugin_file_init"].called


async def test_add_plugin_extra(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试添加额外插件
    """
    from zhenxun.builtin_plugins.plugin_store import _matcher

    init_mocked_api(mocked_api=mocked_api)
    mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        return_value=tmp_path / "zhenxun",
    )

    plugin_id = 3

    async with app.test_matcher(_matcher) as ctx:
        bot = create_bot(ctx)
        bot: Bot = cast(Bot, bot)
        raw_message: str = f"添加插件 {plugin_id}"
        event: GroupMessageEvent = _v11_group_message_event(
            message=raw_message,
            self_id=BotId.QQ_BOT,
            user_id=UserId.SUPERUSER,
            group_id=GroupId.GROUP_ID_LEVEL_5,
            message_id=MessageId.MESSAGE_ID,
            to_me=True,
        )
        ctx.receive_event(bot=bot, event=event)
        ctx.should_call_send(
            event=event,
            message=Message(message=f"正在添加插件 Id: {plugin_id}"),
            result=None,
            bot=bot,
        )
        ctx.should_call_send(
            event=event,
            message=Message(message="插件 github订阅 安装成功! 重启后生效"),
            result=None,
            bot=bot,
        )
    assert mocked_api["basic_plugins"].called
    assert mocked_api["extra_plugins"].called
    assert mocked_api["github_sub_plugin_contents"].called
    assert mocked_api["github_sub_plugin_api"].called
    assert mocked_api["github_sub_plugin_file_init"].called
