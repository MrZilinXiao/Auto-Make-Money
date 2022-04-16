# -*- encoding: utf-8 -*-
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from utils import logger
from ths_trader import THSTrader
from spider import EastSpider
from config import ths_xiadan_path, SCKey
import sys


def job():
    push_message = ''
    try:
        ths_trader = THSTrader(ths_xiadan_path)
        spider = EastSpider()
        today_kzz_list = spider.get_today_list()
        if not today_kzz_list:
            raise ValueError("今日没有可申购的可转债")
        for stock_id, name in today_kzz_list:
            push_message += str(ths_trader.buy(stock_id, 100, 10000)) + '\n'
    except Exception as e:
        push_message += str(e)
    finally:
        r = requests.get('http://sc.ftqq.com/' + SCKey + '.send', params={'text': '今日可转债通知', 'desp': push_message})
        print(r.text)
        logger.info(push_message)


if __name__ == '__main__':
    if sys.argv[1] == 'cron':
        scheduler = BlockingScheduler()
        # scheduler.add_job(job, 'interval', seconds=10)
        scheduler.add_job(job, 'cron', day_of_week='0-6', hour=9, minute=35)
        scheduler.start()
    elif sys.argv[1] == 'test':
        job()
    else:
        pass
