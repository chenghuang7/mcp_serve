#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   weather_tool.py
@Time    :   2025/09/15 22:51:00
@Author  :   SeeStars
@Version :   1.0
@Desc    :   None
"""


import logging
import traceback
import json
import httpx
from setting import settings
from common.types import Language, LANGUAGE_NAMES
from mcp.server import FastMCP
from openai import OpenAI
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register(app: FastMCP):

    @app.tool()
    def generate_image(
        images_prompts: List[str],
        resolution: str = "1024x1024",
    ) -> list[str]:
        """
        @desc     : 生成图片
        @param    : images_prompts
        @param    : resolution 
        @return   :
        """

        image_urls = []
        if resolution:
            resolution = resolution.replace("*", "x")

        llm_client = OpenAI(
            api_key=settings.API_KEY,
            base_url="https://open.bigmodel.cn/api/paas/v4",
            http_client=httpx.Client(proxy=settings.PROXY) if settings.PROXY else None,
        )
        try:
            for prompt in images_prompts:
                safe_prompt = (
                    f"Create a safe, family-friendly illustration. {prompt} "
                    "The image should be appropriate for all ages, non-violent, and non-controversial."
                )
                response = llm_client.images.generate(
                    model="cogview-3-flash",
                    prompt=safe_prompt,
                    size=resolution,
                    quality="standard",
                    n=1,
                )
                url = response.data[0].url
                image_urls.append(url)
                logger.info(f"image generate res: {url}")

        except Exception as e:
            logger.error(f"Failed to generate image: {e}\n{traceback.format_exc()}")
            return ""
        return image_urls

    @app.tool()
    def get_story_prompt(
        story_theme: str = None,
        language: Language = Language.CHINESE_CN,
        segments: int = 3,
    ) -> str:
        """
        @desc     : 根据故事主题生成故事提示词
        @param    : story_prompt (str, optional): 故事提示. Defaults to None.
        @param    : segments (int, optional): 故事分段数. Defaults to 3.
        @return   : 完整的提示词
        """
        languageValue = LANGUAGE_NAMES[language]
        if story_theme:
            base_prompt = f"讲一个故事，主题是：{story_theme}"
        return f"""
        {base_prompt}. The story needs to be divided into {segments} scenes, and each scene must include descriptive text and an image prompt.

        Please return the result in the following JSON format, where the key `list` contains an array of objects:

        **Expected JSON format**:
        {{
            "list": [
                {{
                    "text": "Descriptive text for the scene",
                    "image_prompt": "Detailed image generation prompt, described in English"
                }},
                {{
                    "text": "Another scene description text",
                    "image_prompt": "Another detailed image generation prompt in English"
                }}
            ]
        }}

        **Requirements**:
        1. The root object must contain a key named `list`, and its value must be an array of scene objects.
        2. Each object in the `list` array must include:
            - `text`: A descriptive text for the scene, written in {languageValue}.
            - `image_prompt`: A detailed prompt for generating an image, written in English.
        3. Ensure the JSON format matches the above example exactly. Avoid extra fields or incorrect key names like `cimage_prompt` or `inage_prompt`.

        **Important**:
        - If there is only one scene, the array under `list` should contain a single object.
        - The output must be a valid JSON object. Do not include explanations, comments, or additional content outside the JSON.

        Example output:
        {{
            "list": [
                {{
                    "text": "Scene description text",
                    "image_prompt": "Detailed image generation prompt in English"
                }}
            ]
        }}
        """

    @app.tool()
    async def generate_story(story_prompt: str):
        '''
        @desc     : 根据故事提示词生成故事的每个场景
        @param    : story_prompt (str): 故事场景提示词
        @return   : List[Dict[str, Any]]: 故事场景列表
        '''

        llm_client = OpenAI(api_key=settings.API_KEY, base_url="https://open.bigmodel.cn/api/paas/v4", http_client=httpx.Client(proxy=settings.PROXY))

        messages = [
            {"role": "system", "content": "你是一个专业的故事创作者，善于创作引人入胜的故事。请只返回JSON格式的内容。"},
            {"role": "user", "content": story_prompt},
        ]

        response = llm_client.chat.completions.create(
            model="glm-4-flashx",
            response_format={"type": "json_object"},
            messages=messages,
        )
        content = response.choices[0].message.content
        result = json.loads(content)
        return result
