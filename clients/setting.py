#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   setting.py
@Time    :   2025/09/11 22:16:37
@Author  :   SeeStars
@Version :   1.0
@Desc    :   None
"""


import os
import json
import logging

from pydantic import Field
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    LLM_API_KEY: str = Field("", description="")
    LLM_BASE_URL: str = Field("", description="")
    LLM_MODEL: str = Field("", description="")

    MCP_URL: str = Field("", description="")


settings = Settings(
    _case_sensitive=True,
    _env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
    _env_file_encoding="utf-8",
)


def print_settings(s: Settings):
    raw = s.model_dump()
    display = {}
    for k, v in raw.items():
        if "KEY" in k.upper():  # API_KEY 等敏感信息只显示前后几位
            display[k] = v[:4] + "****" + v[-4:] if v else ""
        else:
            display[k] = v
    logger.info("[Settings Loaded]")
    logger.info(json.dumps(display, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print_settings(settings)
