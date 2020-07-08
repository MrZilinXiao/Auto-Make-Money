# -*- encoding: utf-8 -*-

SCKey = "XXX"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0 "
headers = {'User-Agent': user_agent}
ths_xiadan_path = r'C:\同花顺软件\同花顺\xiadan.exe'


# 请在理解pywin32操作窗口逻辑后，在下面自行适配你的同花顺交易客户端句柄ID
DEFAULT_EXE_PATH: str = ""
TITLE = "网上股票交易系统5.0"

TRADE_SECURITY_CONTROL_ID = 1032
TRADE_PRICE_CONTROL_ID = 1033
TRADE_AMOUNT_CONTROL_ID = 1034

TRADE_SUBMIT_CONTROL_ID = 1006

TRADE_MARKET_TYPE_CONTROL_ID = 1541

COMMON_GRID_CONTROL_ID = 1047

COMMON_GRID_LEFT_MARGIN = 10
COMMON_GRID_FIRST_ROW_HEIGHT = 30
COMMON_GRID_ROW_HEIGHT = 16

BALANCE_MENU_PATH = ["查询[F4]", "资金股票"]
POSITION_MENU_PATH = ["查询[F4]", "资金股票"]
TODAY_ENTRUSTS_MENU_PATH = ["查询[F4]", "当日委托"]
TODAY_TRADES_MENU_PATH = ["查询[F4]", "当日成交"]

BALANCE_CONTROL_ID_GROUP = {
    "资金余额": 1012,
    "可用金额": 1016,
    "可取金额": 1017,
    "股票市值": 1014,
    "总资产": 1015,
}

POP_DIALOD_TITLE_CONTROL_ID = 1365

GRID_DTYPE = {
    "操作日期": str,
    "委托编号": str,
    "申请编号": str,
    "合同编号": str,
    "证券代码": str,
    "股东代码": str,
    "资金帐号": str,
    "资金帐户": str,
    "发生日期": str,
}

CANCEL_ENTRUST_ENTRUST_FIELD = "合同编号"
CANCEL_ENTRUST_GRID_LEFT_MARGIN = 50
CANCEL_ENTRUST_GRID_FIRST_ROW_HEIGHT = 30
CANCEL_ENTRUST_GRID_ROW_HEIGHT = 16

AUTO_IPO_SELECT_ALL_BUTTON_CONTROL_ID = 1098
AUTO_IPO_BUTTON_CONTROL_ID = 1006
AUTO_IPO_MENU_PATH = ["新股申购", "批量新股申购"]
AUTO_IPO_NUMBER = '申购数量'
