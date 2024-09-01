from typing import cast
from pathlib import Path
from collections.abc import Callable

from nonebug import App
from respx import MockRouter
from pytest_mock import MockerFixture
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.message import Message

from tests.config import BotId, UserId, GroupId, MessageId
from tests.utils import (
    get_response_json,
    _v11_group_message_event,
    _v11_private_message_send,
)


def init_mocked_api(mocked_api: MockRouter) -> None:
    mocked_api.get(
        url="https://api.github.com/repos/HibiKier/zhenxun_bot/releases/latest",
        name="release_latest",
    ).respond(json=get_response_json(path="release_latest.json"))
    mocked_api.get(
        url="https://raw.githubusercontent.com/HibiKier/zhenxun_bot/dev/__version__",
        name="dev_branch_version",
    ).respond(text="__version__: v0.2.2")
    mocked_api.get(
        url="https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/__version__",
        name="main_branch_version",
    ).respond(text="__version__: v0.2.2")
    mocked_api.get(
        url="https://api.github.com/repos/HibiKier/zhenxun_bot/tarball/v0.2.2",
        name="release_download_url",
    ).respond(
        status_code=302,
        headers={
            "Location": "https://codeload.github.com/HibiKier/zhenxun_bot/legacy.tar.gz/refs/tags/v0.2.2"
        },
    )
    import io
    import tarfile

    tar_buffer = io.BytesIO()

    from zhenxun.builtin_plugins.auto_update.config import (
        REQ_TXT_FILE,
        PYPROJECT_FILE,
        PYPROJECT_LOCK_FILE,
    )

    # 指定要添加到压缩文件中的文件路径列表
    file_paths: list[Path] = [
        PYPROJECT_FILE,
        PYPROJECT_LOCK_FILE,
        REQ_TXT_FILE,
    ]

    # 打开一个tarfile对象，写入到上面创建的BytesIO对象中
    with tarfile.open(mode="w:gz", fileobj=tar_buffer) as tar:
        _extracted_from_init_mocked_api_43(tarfile, tar, file_paths, io)
    mocked_api.get(
        url="https://codeload.github.com/HibiKier/zhenxun_bot/legacy.tar.gz/refs/tags/v0.2.2",
        name="release_download_url_redirect",
    ).respond(
        content=tar_buffer.getvalue(),
    )


# TODO Rename this here and in `init_mocked_api`
def _extracted_from_init_mocked_api_43(tarfile, tar, file_paths, io):
    folder_name = "my_folder"
    tarinfo = tarfile.TarInfo(folder_name)
    tarinfo.type = tarfile.DIRTYPE
    tarinfo.mode = 0o755
    tar.addfile(tarinfo)

    # 读取并添加指定的文件
    for file_path in file_paths:
        # 读取文件内容
        with open(file_path, "rb") as file:
            file_content = file.read()

        # 使用BytesIO创建文件内容
        file_buffer = io.BytesIO(file_content)

        # 创建TarInfo对象
        tarinfo = tarfile.TarInfo(
            f"{folder_name}/{file_path.name}"
        )  # 使用文件名作为tar中的名字
        tarinfo.mode = 0o644  # 设置文件夹权限
        tarinfo.size = len(file_content)

        # 添加文件
        tar.addfile(tarinfo, fileobj=file_buffer)


async def test_check_update_release(
    app: App,
    mocker: MockerFixture,
    mocked_api: MockRouter,
    create_bot: Callable,
    tmp_path: Path,
) -> None:
    """
    测试检查更新
    """
    from zhenxun.builtin_plugins.auto_update import _matcher

    init_mocked_api(mocked_api=mocked_api)

    mocker.patch(
        "zhenxun.builtin_plugins.auto_update._data_source.REPLACE_FOLDERS",
        return_value=[],
    )
    mocker.patch(
        "zhenxun.builtin_plugins.auto_update._data_source.install_requirement",
        return_value=None,
    )

    async with app.test_matcher(_matcher) as ctx:
        bot = create_bot(ctx)
        bot = cast(Bot, bot)
        raw_message = "检查更新 release"
        event = _v11_group_message_event(
            raw_message,
            self_id=BotId.QQ_BOT,
            user_id=UserId.SUPERUSER,
            group_id=GroupId.GROUP_ID_LEVEL_5,
            message_id=MessageId.MESSAGE_ID,
            to_me=True,
        )
        ctx.receive_event(bot, event)
        ctx.should_call_api(
            "send_msg",
            _v11_private_message_send(
                message="检测真寻已更新，版本更新：v0.2.2 -> v0.2.2\n开始更新...",
                user_id=UserId.SUPERUSER,
            ),
        )
        ctx.should_call_send(
            event=event,
            message=Message(
                "版本更新完成\n" "版本: v0.2.2 -> v0.2.2\n" "请重新启动真寻以完成更新!"
            ),
            result=None,
            bot=bot,
        )
        ctx.should_finished(_matcher)
    assert mocked_api["release_latest"].called
    assert mocked_api["release_download_url"].called
    assert mocked_api["release_download_url_redirect"].called
