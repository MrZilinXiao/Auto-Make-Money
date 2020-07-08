# -*- encoding: utf-8 -*-
"""
@File    : utils.py
@Time    : 2020/7/8 15:39
@Author  : MrZilinXiao
@Email   : me@mrxiao.net
@Software: PyCharm
"""
import logging

logger = logging.getLogger("Auto-KZZ")
logger.setLevel(logging.INFO)
logger.propagate = False

fmt = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(filename)s %(lineno)s: %(message)s"
)
ch = logging.StreamHandler()

ch.setFormatter(fmt)
logger.handlers.append(ch)