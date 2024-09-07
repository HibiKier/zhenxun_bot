from .models import RepoInfo
from .consts import GITHUB_REPO_URL_PATTERN
from .func import get_fastest_raw_format, get_fastest_archive_format

__all__ = [
    "parse_github_url",
    "get_fastest_raw_format",
    "get_fastest_archive_format",
]


def parse_github_url(github_url: str) -> "RepoInfo":
    if matched := GITHUB_REPO_URL_PATTERN.match(github_url):
        return RepoInfo(**{k: v for k, v in matched.groupdict().items() if v})
    raise ValueError("github地址格式错误")
