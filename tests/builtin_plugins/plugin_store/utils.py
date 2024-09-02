# ruff: noqa: ASYNC230

from pathlib import Path

from respx import MockRouter

from tests.utils import get_content_bytes as _get_content_bytes
from tests.utils import get_response_json as _get_response_json


def get_response_json(file: str) -> dict:
    return _get_response_json(Path() / "plugin_store", file=file)


def get_content_bytes(file: str) -> bytes:
    return _get_content_bytes(Path() / "plugin_store", file)


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
    ).respond(content=get_content_bytes("search_image.py"))
    mocked_api.get(
        "https://raw.githubusercontent.com/zhenxun-org/zhenxun_bot_plugins/main/plugins/alapi/jitang.py",
        name="jitang_plugin_file",
    ).respond(content=get_content_bytes("jitang.py"))
    mocked_api.get(
        "https://raw.githubusercontent.com/xuanerwa/zhenxun_github_sub/main/github_sub/__init__.py",
        name="github_sub_plugin_file_init",
    ).respond(content=get_content_bytes("github_sub.py"))
