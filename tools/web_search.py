#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   web_search.py
@Time    :   2025/09/11 21:43:07
@Author  :   SeeStars 
@Version :   1.0
@Desc    :   None
'''

import logging
import traceback
import httpx
from setting import settings

def register(app):
    @app.tool()
    async def web_search(query: str) -> dict:
        """
            搜索互联网内容

            Args:
                query: 要搜索内容

            Returns:
                搜索结果的总结
        """
        try:
            logging.info(f"web_search called. query={query!r}")

            api_key = settings.API_KEY
            header_value = f"Bearer {api_key}" if api_key else ""
            headers = {"Authorization": header_value}

            payload = {
                "tool": "web-search-pro",
                "messages": [{"role": "user", "content": query}],
                "stream": False
            }

            async with httpx.AsyncClient(
                proxy=settings.PROXY,
                timeout=30.0
            ) as client:
                resp = await client.post(
                    "https://open.bigmodel.cn/api/paas/v4/tools",
                    headers=headers,
                    json=payload
                )

            if resp.status_code != 200:
                return {"result": f"HTTP {resp.status_code}: {resp.text[:500]}"}

            j = resp.json()
            choices = j.get("choices", [])
            result = "\n\n".join(
                c.get("message", {}).get("content", "")
                for c in choices if c.get("message")
            )
            return {"result": result or str(j)[:1000]}

        except Exception:
            tb = traceback.format_exc()
            logging.error("web_search 异常", exc_info=True)
            return {"result": f"EXCEPTION: {tb}"}
