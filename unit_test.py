# -*- encoding: utf-8 -*-
"""
@File    : unit_test.py
@Time    : 2020/7/8 17:07
@Author  : MrZilinXiao
@Email   : me@mrxiao.net
@Software: PyCharm
"""
import unittest
from spider import EastSpider


class TestEastSpider(unittest.TestCase):
    def test_today_stock_list(self):
        spider = EastSpider()
        print(spider.get_today_list())

