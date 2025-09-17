#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   stdio_client.py
@Time    :   2025/09/11 21:47:05
@Author  :   SeeStars
@Version :   1.0
@Desc    :   None
"""

import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

from fastmcp import Client

server_params = StdioServerParameters(
    command="uv",
    args=["run", "main.py"],
    # env=None
)

async def mcp_main():
    async with stdio_client(server_params) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(tools)
            response = await session.call_tool("web_search", {"query": "今天杭州天气"})
            print(response)
            
async def fastmcp_main():
    client = Client("main.py")
    
    async with client:
        await client.ping()
        
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        for tool in tools:
            print(tool.name)
        #     story_prompt: str = None,
        # language: Language = Language.CHINESE_CN,
        # segments: int = 3,
        story_prompt = await client.call_tool("get_story_prompt", {"story_prompt": "白色的小兔子"})
        
        story_prompt = story_prompt.content[0].text
        
        result = await client.call_tool("generate_story", {"story_prompt": story_prompt})

        print(type(result.content[0].text))
        
        images_prompt = result.content[0].text["list"]

        for item in images_prompt:
            print(item["image_prompt"])

if __name__ == "__main__":
    asyncio.run(fastmcp_main())
    # asyncio.run(mcp_main())
