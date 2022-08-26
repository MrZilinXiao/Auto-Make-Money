# -*- encoding: utf-8 -*-
"""
爬取来自东方财富网的最新可转债信息：http://data.eastmoney.com/kzz/default.html
接口示例：http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB2.0&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=1&ps=6
"""
import re

from config import headers
import abc
import requests
import json
import time


class BaseSpider(abc.ABC):
    def __init__(self, url=None):
        pass

    def _get_token(self) -> str:
        pass

    def get_today_list(self) -> list:
        pass


# Outdated Spider
# class EastSpider(BaseSpider):
#     def __init__(self, ps='50', url='http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get'):
#         super(EastSpider, self).__init__()
#         self.url = url
#         self.params = {
#             'type': 'KZZ_LB2.0',
#             'token': '',
#             'cmd': '',
#             'st': 'STARTDATE',
#             'sr': '-1',
#             'p': '1',
#             'ps': ps  # page_size
#         }
#
#     def get_list(self):
#         self.params['token'] = self._get_token()
#         r = requests.get(self.url, params=self.params, headers=headers)
#         return json.loads(r.text)
#
#     def get_today_list(self) -> list:
#         r_list = self.get_list()
#         today_str = time.strftime("%Y-%m-%d", time.localtime())
#         today_list = []
#         for stock in r_list:
#             if stock['STARTDATE'].split('T')[0] == today_str:
#                 today_list.append([stock['CORRESCODE'], stock['SNAME']])
#         return today_list
#
#     def _get_token(self) -> str:
#         token_url = 'http://data.eastmoney.com/kzz/default.html'
#         r = requests.get(token_url, headers=headers)
#         token_list = re.findall('&token=(.+?)&', r.text)
#         if len(token_list) != 1:
#             raise ValueError("Token获取出错！")
#         return token_list[0]

# New Example GET request:
# https://datacenter-web.eastmoney.com/api/data/v1/get
# ?sortColumns=PUBLIC_START_DATE
# &sortTypes=-1
# &pageSize=50
# &pageNumber=1
# &reportName=RPT_BOND_CB_LIST
# &columns=ALL

class EastSpider(BaseSpider):
    # 新东方财富网API移除了token验证字段，感谢！
    def __init__(self, url='https://datacenter-web.eastmoney.com/api/data/v1/get'):
        super(EastSpider, self).__init__()
        self.url = url
        self.params = {
            'sortColumns': 'PUBLIC_START_DATE',
            'sortTypes': '-1',
            'pageSize': '10',
            'pageNumber': '1',
            'reportName': 'RPT_BOND_CB_LIST',
            'columns': 'ALL',
            'source': 'WEB',
            'client': 'WEB'
        }

    def get_list(self):
        r = requests.get(self.url, params=self.params, headers=headers)
        ret_dict = json.loads(r.text)
        try:
            data: list = ret_dict['result']['data']
            return data
        except KeyError:
            raise RuntimeError('API解析错误')

    def get_today_list(self) -> list:
        try:
            r_list = self.get_list()
        except RuntimeError as e:  # API偶尔解析错误，直接返回空list
            print(str(e))
            return []
        today_str = time.strftime("%Y-%m-%d", time.localtime())
        # today_str = '2021-07-15'
        today_list = []
        for stock in r_list:
            if stock['VALUE_DATE'].split(' ')[0] == today_str:
                today_list.append([stock['CORRECODE'], stock['SECURITY_NAME_ABBR']])
        return today_list


if __name__ == '__main__':
    spider = EastSpider()
    print(spider.get_list())
