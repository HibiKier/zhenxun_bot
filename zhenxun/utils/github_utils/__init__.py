from .consts import GITHUB_REPO_URL_PATTERN
from .func import get_fastest_raw_format, get_fastest_archive_format
from .models import RepoAPI, RepoInfo, GitHubStrategy, JsdelivrStrategy

__all__ = [
    "parse_github_url",
    "get_fastest_raw_format",
    "get_fastest_archive_format",
    "api_strategy",
]


def parse_github_url(github_url: str) -> "RepoInfo":
    if matched := GITHUB_REPO_URL_PATTERN.match(github_url):
        return RepoInfo(**{k: v for k, v in matched.groupdict().items() if v})
    raise ValueError("github地址格式错误")


# 使用
jsdelivr_api = RepoAPI(JsdelivrStrategy())  # type: ignore
github_api = RepoAPI(GitHubStrategy())  # type: ignore

api_strategy = [github_api, jsdelivr_api]
