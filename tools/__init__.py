#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2025/09/11 21:43:13
@Author  :   SeeStars
@Version :   1.0
@Desc    :   None
"""
from mcp.server import FastMCP
from . import web_search
from . import math_tool


def register_tools(app: FastMCP):
    """
    @desc     : 集中注册所有工具
    @param    : app (FastMCP): FastMCP 应用实例
    """
    web_search.register(app)
    math_tool.register(app)
