#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sse_client.py
@Time    :   2025/09/12 09:24:58
@Author  :   SeeStars 
@Version :   1.0
@Desc    :   None
'''

import asyncio
from mcp.client.sse import sse_client
from mcp import ClientSession
from fastmcp import Client

from setting import settings

client = Client(settings.MCP_URL)

async def fastmcp_main():
    async with client:
        await client.ping()
        
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        
        print(tools)
        print(resources)
        print(prompts)

        response = await client.call_tool("web_search", {"query": "今天杭州天气"})
        print(response)


async def mcp_main():
    async with sse_client(settings.MCP_URL) as (sse, write):
        async with ClientSession(sse, write) as session:
            await session.initialize()
            response = await session.list_tools()
            print(response)
            response = await session.call_tool("web_search", {"query": "今天杭州天气"})
            print(response)

if __name__ == "__main__":
    asyncio.run(fastmcp_main())
