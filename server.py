# server.py
import logging
from fastmcp import FastMCP
import asyncio

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")

# 创建 FastMCP 实例
mcp = FastMCP("Demo")

# 使用 @mcp.tool 装饰器注册工具
@mcp.tool
async def greet(name: str) -> str:
    """返回问候语"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=5000)
