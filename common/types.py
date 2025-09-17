#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   types.py
@Time    :   2025/09/15 23:13:44
@Author  :   SeeStars 
@Version :   1.0
@Desc    :   None
'''

from enum import Enum


class Language(str, Enum):
    """支持的语言"""
    CHINESE_CN = "zh-CN"      # 中文（简体）
    CHINESE_TW = "zh-TW"      # 中文（繁体）
    ENGLISH_US = "en-US"      # 英语（美国）
    JAPANESE = "ja-JP"        # 日语
    KOREAN = "ko-KR"          # 韩语
    
LANGUAGE_NAMES = {
    Language.CHINESE_CN: "中文（简体）",
    Language.CHINESE_TW: "中文（繁体）",
    Language.ENGLISH_US: "English",
    Language.JAPANESE: "日本語",
    Language.KOREAN: "한국어"
}