#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Time    :   2025/09/11 21:42:59
@Author  :   SeeStars
@Version :   1.0
@Desc    :   None
"""


import logging
from mcp.server import FastMCP
from tools import register_tools
from setting import settings

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")

logger = logging.getLogger(__name__)

app = FastMCP(
    "mcp-serve",
    host=settings.MCP_HOST,
    port=settings.MCP_PORT,
)

register_tools(app)

if __name__ == "__main__":
    transport = settings.MCP_TRANSPORT
    if transport == "sse":
        app.run(transport=transport)
    elif transport == "stdio":
        app.run(transport=transport)
