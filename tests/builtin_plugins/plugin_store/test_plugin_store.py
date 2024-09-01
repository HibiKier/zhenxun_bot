# ruff: noqa: ASYNC230

from typing import cast
from pathlib import Path
from collections.abc import Callable

from nonebug import App
from respx import MockRouter
from pytest_mock import MockerFixture
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent

from tests.utils import _v11_group_message_event
from tests.config import BotId, UserId, GroupId, MessageId
from tests.utils import get_response_json as _get_response_json


def get_response_json(file: str) -> dict:
    return _get_response_json(Path() / "plugin_store", file=file)


def init_mocked_api(mocked_api: MockRouter) -> None:
    mocked_api.get(
        "https://data.jsdelivr.com/v1/packages/gh/xuanerwa/zhenxun_github_sub@main",
        name="github_sub_plugin_metadata",
    ).respond(json=get_response_json("github_sub_plugin_metadata.json"))
    mocked_api.get(
        "https://data.jsdelivr.com/v1/packages/gh/zhenxun-org/zhenxun_bot_plugins@main",
        name="zhenxun_bot_plugins_metadata",
    ).respond(json=get_response_json("zhenxun_bot_plugins_metadata.json"))
    mocked_api.get(
        "https://cdn.jsdelivr.net/gh/zhenxun-org/zhenxun_bot_plugins/plugins.json",
        name="basic_plugins",
    ).respond(200, json=get_response_json("basic_plugins.json"))
    mocked_api.get(
        "https://raw.githubusercontent.com/zhenxun-org/zhenxun_bot_plugins_index/index/plugins.json",
        name="extra_plugins",
    ).respond(200, json=get_response_json("extra_plugins.json"))
    mocked_api.get(
        "https://raw.githubusercontent.com/zhenxun-org/zhenxun_bot_plugins/main/plugins/search_image/__init__.py",
        name="search_image_plugin_file_init",
    ).respond(content=b"")
    mocked_api.get(
        "https://raw.githubusercontent.com/zhenxun-org/zhenxun_bot_plugins/main/plugins/alapi/jitang.py",
        name="jitang_plugin_file",
    ).respond(content=b"")
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
    mock_base_path = mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        new=tmp_path / "zhenxun",
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
    assert mocked_api["zhenxun_bot_plugins_metadata"].called
    assert mocked_api["search_image_plugin_file_init"].called
    assert (mock_base_path / "plugins" / "search_image" / "__init__.py").is_file()


async def test_add_plugin_basic_is_not_dir(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试添加基础插件，插件不是目录
    """
    from zhenxun.builtin_plugins.plugin_store import _matcher

    init_mocked_api(mocked_api=mocked_api)
    mock_base_path = mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        new=tmp_path / "zhenxun",
    )

    plugin_id = 0

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
            message=Message(message="插件 鸡汤 安装成功! 重启后生效"),
            result=None,
            bot=bot,
        )
    assert mocked_api["basic_plugins"].called
    assert mocked_api["extra_plugins"].called
    assert mocked_api["zhenxun_bot_plugins_metadata"].called
    assert mocked_api["jitang_plugin_file"].called
    assert (mock_base_path / "plugins" / "alapi" / "jitang.py").is_file()


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
    mock_base_path = mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        new=tmp_path / "zhenxun",
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
    assert mocked_api["github_sub_plugin_metadata"].called
    assert mocked_api["github_sub_plugin_file_init"].called
    assert (mock_base_path / "plugins" / "github_sub" / "__init__.py").is_file()


async def test_update_plugin_basic(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试更新基础插件
    """
    from zhenxun.builtin_plugins.plugin_store import _matcher

    init_mocked_api(mocked_api=mocked_api)
    mock_base_path = mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        new=tmp_path / "zhenxun",
    )

    plugin_id = 1

    async with app.test_matcher(_matcher) as ctx:
        bot = create_bot(ctx)
        bot: Bot = cast(Bot, bot)
        raw_message = f"更新插件 {plugin_id}"
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
            message=Message(message=f"正在更新插件 Id: {plugin_id}"),
            result=None,
            bot=bot,
        )
        ctx.should_call_send(
            event=event,
            message=Message(message="插件 识图 更新成功! 重启后生效"),
            result=None,
            bot=bot,
        )
    assert mocked_api["basic_plugins"].called
    assert mocked_api["extra_plugins"].called
    assert mocked_api["zhenxun_bot_plugins_metadata"].called
    assert mocked_api["search_image_plugin_file_init"].called
    assert (mock_base_path / "plugins" / "search_image" / "__init__.py").is_file()


async def test_remove_plugin(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试删除插件
    """
    from zhenxun.builtin_plugins.plugin_store import _matcher

    init_mocked_api(mocked_api=mocked_api)
    mock_base_path = mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        new=tmp_path / "zhenxun",
    )

    plugin_path = mock_base_path / "plugins" / "search_image"
    plugin_path.mkdir(parents=True, exist_ok=True)

    with open(plugin_path / "__init__.py", "w") as f:
        f.write("")

    plugin_id = 1

    async with app.test_matcher(_matcher) as ctx:
        bot = create_bot(ctx)
        bot: Bot = cast(Bot, bot)
        raw_message = f"移除插件 {plugin_id}"
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
            message=Message(message="插件 识图 移除成功! 重启后生效"),
            result=None,
            bot=bot,
        )
    assert mocked_api["basic_plugins"].called
    assert mocked_api["extra_plugins"].called
    assert not (mock_base_path / "plugins" / "search_image" / "__init__.py").is_file()
