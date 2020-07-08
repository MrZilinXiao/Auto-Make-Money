# -*- encoding: utf-8 -*-
"""
@File    : interest_cal.py
@Time    : 2020/7/8 18:26
@Author  : MrZilinXiao
@Email   : me@mrxiao.net
@Software: PyCharm
"""
from spider import EastSpider

spider = EastSpider('91')  # 最近91支可转债 对应2020年1月至今约6个月可供申购的可转债
kzz_list = spider.get_list()
expectation = 0.0
for kzz in kzz_list:
    try:
        luck_rate = kzz['LUCKRATE'] * 1000 * 0.01  # 每10张对应一组配号，顶格申购是10000张，中一签的概率约为LUCKRATE*1000*0.01
        expectation += luck_rate * 200
    except:
        continue  # 最新的转债中签率未公布

print(expectation)

#  结果 约1800
