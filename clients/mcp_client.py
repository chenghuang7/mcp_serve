#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   MCPClient.py
@Time    :   2025/09/11 21:57:10
@Author  :   SeeStars
@Version :   1.1
@Desc    :   MCP + LLM 集成，支持工具调用
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
    """
    @name     : MCPClient
    @desc     : 管理 MCP 会话和工具调用
    """

    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect(self, command: str = "uv", args: Optional[list] = None):
        """
        @desc     : 连接到 MCP 服务器
        @param    : command (str): 服务器命令
                    args (list): 命令参数
        """
        if args is None:
            args = ["run", "main.py"]

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
    """
    @name     : LLMHandler
    @desc     : 负责 LLM 调用及 function call 处理
    """

    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.system_prompt = "You are a helpful assistant."

    def build_messages(self, user_query: str, context=None):
        messages = [{"role": "system", "content": self.system_prompt}]
        if context:
            messages.extend(context)
        return messages

    async def ask(self, query: str, available_tools: list, context=None):
        messages = self.build_messages(query, context)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=available_tools,
        )
        return response.choices[0]


class ChatEngine:
    """
    @name     : ChatEngine
    @desc     : 将 MCPClient 与 LLMHandler 组合，处理完整问答流程
    """

    def __init__(self, mcp_client: MCPClient, llm_handler: LLMHandler):
        self.mcp_client = mcp_client
        self.llm_handler = llm_handler
        self.messages = []

    async def process_query(self, query: str) -> str:
        # 获取工具列表
        tools_response = await self.mcp_client.list_tools()
        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                },
            }
            for t in tools_response.tools
        ]

        self.llm_handler.system_prompt = """
            You are a helpful assistant that can use tools.

            Your rules:
            1. You MUST use the available tools (such as `web_search`, `get_story_prompt`, `generate_story`, `generate_image`) whenever they can answer the user's question.
            - DO NOT answer directly if a tool can handle it.
            2. If the user's question is about factual or time-sensitive info, you MUST call the `web_search` tool.
            3. If the user's question is about generating a story, theme, or image, you MUST call the corresponding story or image generation tool.
            4. Only when NO relevant tool is available are you allowed to answer directly.
            5. Always preserve the user's original question when passing parameters to tools. Do not drop details or change meaning.
        """

        content = await self.llm_handler.ask(query, available_tools, context=self.messages)

        while content.finish_reason == "tool_calls":
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            self.messages.append(
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [call.model_dump() for call in content.message.tool_calls],
                }
            )

            result = await self.mcp_client.call_tool(tool_name, tool_args)

            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": "\n".join(c.text for c in result.content if hasattr(c, "text")),
                }
            )
            content = await self.llm_handler.ask(query, available_tools, context=self.messages)
        self.messages.append({"role": "assistant", "content": content.message.content})
        return content.message.content

    def print_history(self, messages):
        """
        @description : 打印对话历史
        """
        print("\n=== 对话历史 ===")
        for i, msg in enumerate(messages, 1):
            role = msg.get("role", "unknown")

            if role == "user":
                print(f"[用户 {i}] {msg.get('content')}")

            elif role == "assistant":
                if msg.get("content"):
                    print(f"[助手 {i}] {msg.get('content')}")
                if "tool_calls" in msg:
                    for call in msg["tool_calls"]:
                        tool_type = call.get("type", "")
                        if tool_type == "function":
                            fn = call.get("function", {})
                            print(f"[助手调用工具 {i}] {fn.get('name')} 参数: {fn.get('arguments')}")

            elif role == "tool":
                print(f"[工具结果 {i}] {msg.get('content')}")

        print("================\n")

    async def chat_loop(self):
        while True:
            self.print_history(self.messages)
            query = input("\nQuery: ").strip()
            if query.lower() in ("quit", "exit"):
                break
            elif len(query) < 1:
                continue
            try:
                self.messages.append(
                    {
                        "role": "user",
                        "content": query,
                    }
                )
                response = await self.process_query(query)

            except Exception as e:
                logger.exception("Error processing query")


async def main():
    """
    @description : 初始化 MCPClient、LLMHandler 和 ChatEngine
    """
    mcp_client = MCPClient()
    llm_handler = LLMHandler(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
    )
    chat_engine = ChatEngine(mcp_client, llm_handler)

    try:
        await mcp_client.connect()
        await chat_engine.chat_loop()
    finally:
        await mcp_client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
