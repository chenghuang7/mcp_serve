#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   MCPClient.py
@Time    :   2025/09/11 21:57:10
@Author  :   SeeStars
@Version :   1.0
@Desc    :   None
"""
import json
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
import logging

from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from setting import settings

logger = logging.getLogger(__name__)


class MCPClient:
    '''
    @name     : MCPClient
    @desc     : 管理 MCP 会话和工具调用
    '''

    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect(self, command="uv", args=["run", "main.py"]):
        '''
        @desc     : 连接到 MCP 服务器
        @param    : command (str): 服务器命令
                    args (list): 命令参数
        @return   : 
        '''
        server_params = StdioServerParameters(command=command, args=args, env=None)
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await self.session.initialize()

    async def list_tools(self):
        return await self.session.list_tools()

    async def call_tool(self, tool_name: str, tool_args: dict):
        logger.info(f"Calling tool {tool_name} with args {tool_args}")
        return await self.session.call_tool(tool_name, tool_args)

    async def cleanup(self):
        await self.exit_stack.aclose()


class LLMHandler:
    '''
    @name     : LLMHandler
    @desc     : 负责 LLM 调用及 function call 处理
    '''

    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.system_prompt = (
            "You are a helpful assistant."
            "You have the function of online search. "
            "Please MUST call web_search tool to search the Internet content before answering."
            "Please do not lose the user's question information when searching,"
            "and try to maintain the completeness of the question content as much as possible."
            "When there is a date related question in the user's question,"
            "please use the search function directly to search and PROHIBIT inserting specific time."
        )

    def build_messages(self, user_query: str, context=None):
        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_query}]
        if context:
            messages.extend(context)
        return messages

    async def ask(self, query: str, available_tools: list, context=None):
        messages = self.build_messages(query, context)
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, tools=available_tools
        )
        return response.choices[0]


class ChatEngine:
    '''
    @name     : ChatEngine
    @desc     : 将 MCPClient 与 LLMHandler 组合，处理完整问答流程
    '''
    def __init__(self, mcp_client: MCPClient, llm_handler: LLMHandler):
        self.mcp_client = mcp_client
        self.llm_handler = llm_handler
        self.messages = []

    async def process_query(self, query: str) -> str:
        # 获取工具列表
        tools_response = await self.mcp_client.list_tools()
        available_tools = [
            {"type": "function", "function": {"name": t.name, "description": t.description, "input_schema": t.inputSchema}}
            for t in tools_response.tools
        ]

        # 调用 LLM
        content = await self.llm_handler.ask(query, available_tools, context=self.messages)

        # 如果需要工具调用
        if content.finish_reason == "tool_calls":
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            result = await self.mcp_client.call_tool(tool_name, tool_args)

            # 保存上下文
            self.messages.append(content.message.model_dump())
            self.messages.append({
                "role": "tool",
                "content": result.content[0].text,
                "tool_call_id": tool_call.id
            })

            # 再次调用 LLM 生成最终回答
            final_content = await self.llm_handler.ask(query, available_tools, context=self.messages)
            return final_content.message.content

        return content.message.content

    async def chat_loop(self):
        while True:
            query = input("\nQuery: ").strip()
            if query.lower() == "quit":
                break
            try:
                response = await self.process_query(query)
                print("\n" + response)
            except Exception as e:
                logger.exception("Error processing query")


async def main():
    '''
    @description : 初始化 MCPClient、LLMHandler 和 ChatEngine
    '''
    mcp_client = MCPClient()
    llm_handler = LLMHandler(api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL, model=settings.LLM_MODEL)
    chat_engine = ChatEngine(mcp_client, llm_handler)

    try:
        await mcp_client.connect()
        await chat_engine.chat_loop()
    finally:
        await mcp_client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
