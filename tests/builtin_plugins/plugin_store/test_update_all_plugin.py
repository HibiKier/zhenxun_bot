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
from tests.builtin_plugins.plugin_store.utils import init_mocked_api


async def test_update_all_plugin_basic_need_update(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试更新基础插件，插件需要更新
    """
    from zhenxun.builtin_plugins.plugin_store import _matcher

    init_mocked_api(mocked_api=mocked_api)
    mock_base_path = mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        new=tmp_path / "zhenxun",
    )
    mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.ShopManage.get_loaded_plugins",
        return_value=[("search_image", "0.0")],
    )


    async with app.test_matcher(_matcher) as ctx:
        bot = create_bot(ctx)
        bot: Bot = cast(Bot, bot)
        raw_message = "更新全部插件"
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
            message=Message(message="正在更新全部插件"),
            result=None,
            bot=bot,
        )
        ctx.should_call_send(
            event=event,
            message=Message(message="已更新插件 识图\n共计1个插件! 重启后生效"),
            result=None,
            bot=bot,
        )
    assert mocked_api["basic_plugins"].called
    assert mocked_api["extra_plugins"].called
    assert mocked_api["search_image_plugin_file_init"].called
    assert (mock_base_path / "plugins" / "search_image" / "__init__.py").is_file()


async def test_update_all_plugin_basic_is_new(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试更新基础插件，插件是最新版
    """
    from zhenxun.builtin_plugins.plugin_store import _matcher

    init_mocked_api(mocked_api=mocked_api)
    mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.BASE_PATH",
        new=tmp_path / "zhenxun",
    )
    mocker.patch(
        "zhenxun.builtin_plugins.plugin_store.data_source.ShopManage.get_loaded_plugins",
        return_value=[("search_image", "0.1")],
    )


    async with app.test_matcher(_matcher) as ctx:
        bot = create_bot(ctx)
        bot: Bot = cast(Bot, bot)
        raw_message = "更新全部插件"
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
            message=Message(message="正在更新全部插件"),
            result=None,
            bot=bot,
        )
        ctx.should_call_send(
            event=event,
            message=Message(message="全部插件已是最新版本"),
            result=None,
            bot=bot,
        )
    assert mocked_api["basic_plugins"].called
    assert mocked_api["extra_plugins"].called
