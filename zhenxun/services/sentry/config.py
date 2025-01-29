from typing import Any

from nonebot import get_driver
from nonebot.compat import PYDANTIC_V2, ConfigDict
from pydantic import BaseModel, Field
from sentry_sdk.integrations import Integration
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.loguru import LoguruIntegration

from .compat import model_validator

driver = get_driver()


class Config(BaseModel):
    sentry_dsn: str | None = None
    sentry_environment: str = driver.env
    sentry_integrations: list[Integration] = Field(
        default_factory=lambda: [
            LoguruIntegration(),
            FastApiIntegration(),
            HttpxIntegration(),
            AsyncioIntegration(),
        ]
    )

    # [FIXED] https://github.com/getsentry/sentry-python/issues/653
    # sentry_default_integrations: bool = False

    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    else:

        class Config:
            extra = "allow"
            arbitrary_types_allowed = True

    @model_validator(mode="before")
    @classmethod
    def filter_sentry_configs(cls, values: dict[str, Any]):
        return {
            key: value for key, value in values.items() if key.startswith("sentry_")
        }

    # [FIXED] https://github.com/getsentry/sentry-python/pull/2671
    # LoguruIntegration is auto enabled by sentry_sdk now
    # @field_validator("sentry_integrations", mode="after")
    # def validate_integrations(cls, v: list[Integration]):
    #     ids = {i.identifier for i in v}
    #     if LoguruIntegration.identifier not in ids:
    #         v.append(LoguruIntegration())
    #     return v
