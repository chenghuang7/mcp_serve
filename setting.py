#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setting.py
@Time    :   2025/09/11 20:54:28
@Author  :   SeeStars 
@Version :   1.0
@Desc    :   None
'''

import os
import json
from pydantic import Field
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    '''
    @name     : Settings
    @desc     : 全局配置
    '''

    API_KEY: str = Field("", description="调用 BigModel 的 API Key")
    PROXY: str | None = Field(None, description="代理地址，例如 http://127.0.0.1:7890")
    MCP_TRANSPORT: str = Field("stdio", description="MCP 传输方式: stdio 或 tcp")
    MCP_HOST: str = Field("0.0.0.0", description="MCP TCP 模式下的监听地址")
    MCP_PORT: int = Field(5000, description="MCP TCP 模式下的监听端口")

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

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
