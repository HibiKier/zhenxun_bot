from collections.abc import Generator

from .const import GITHUB_REPO_URL_PATTERN
from .func import get_fastest_archive_formats, get_fastest_raw_formats
from .models import GitHubStrategy, JsdelivrStrategy, RepoAPI, RepoInfo

__all__ = [
    "GithubUtils",
    "get_fastest_archive_formats",
    "get_fastest_raw_formats",
]


class GithubUtils:
    # 使用
    jsdelivr_api = RepoAPI(JsdelivrStrategy())  # type: ignore
    github_api = RepoAPI(GitHubStrategy())  # type: ignore

    @classmethod
    def iter_api_strategies(cls) -> Generator[RepoAPI]:
        yield from [cls.github_api, cls.jsdelivr_api]

    @classmethod
    def parse_github_url(cls, github_url: str) -> "RepoInfo":
        if matched := GITHUB_REPO_URL_PATTERN.match(github_url):
            return RepoInfo(**{k: v for k, v in matched.groupdict().items() if v})
        raise ValueError("github地址格式错误")
