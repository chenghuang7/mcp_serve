#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   math_tool.py
@Time    :   2025/09/12 11:26:50
@Author  :   SeeStars 
@Version :   1.0
@Desc    :   None
'''
import logging
import traceback
import httpx
from setting import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register(app):
    @app.tool()
    def add(a: float, b: float) -> float:
        '''
        @desc     : Adds two numbers.
        @param    : a (float): The first number.
                    b (float): The second number.
        @return   : float: The sum of a and b.
        '''
        return a + b

    @app.tool()
    def subtract(a: float, b: float) -> float:
        '''
        @desc     : Subtracts two numbers.
        @param    : a (float): The first number.
                    b (float): The second number.
        @return   : float: The difference of a and b.
        '''
        return a - b

    @app.tool()
    def multiply(a: float, b: float) -> float:
        '''
        @desc     : Multiplies two numbers.
        @param    : a (float): The first number.
                    b (float): The second number.
        @return   : float: The product of a and b.
        '''
        return a * b

    @app.tool()
    def divide(a: float, b: float) -> float:
        '''
        @desc     : Divides two numbers.
        @param    : a (float): The first number.
                    b (float): The second number.
        @return   : float: The quotient of a and b.
        '''
        if b == 0:
            return float("inf")
        return a / b
