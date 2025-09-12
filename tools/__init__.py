#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2025/09/11 21:43:13
@Author  :   SeeStars 
@Version :   1.0
@Desc    :   None
'''

from . import web_search
from . import math_tool

def register_tools(app):
    """集中注册所有工具"""
    web_search.register(app)
    math_tool.register(app)
