# -*- encoding: utf-8 -*-
"""
同花顺通用wrapper 来自easytrader
link： https://github.com/shidenggui/easytrader

"""
import abc
import functools
import logging
import time

import pywinauto
from pywinauto import findwindows, timings

import config
from utils import logger
import re
from typing import Optional

from pywinauto import win32defines
from pywinauto.win32functions import SetForegroundWindow, ShowWindow


class TradeError(IOError):
    pass


def get_code_type(code):
    """
    判断代码是属于那种类型，目前仅支持 ['fund', 'stock']
    :return str 返回code类型, fund 基金 stock 股票
    """
    if code.startswith(('00', '30', '60')):
        return 'stock'
    return 'fund'


def round_price_by_code(price, code):
    """
    根据代码类型[股票，基金] 截取制定位数的价格
    :param price: 证券价格
    :param code: 证券代码
    :return: str 截断后的价格的字符串表示
    """
    if isinstance(price, str):
        return price

    typ = get_code_type(code)
    if typ == 'fund':
        return '{:.3f}'.format(price)
    return '{:.2f}'.format(price)


class PopDialogHandler:
    def __init__(self, app):
        self._app = app

    @staticmethod
    def _set_foreground(window):
        if window.has_style(win32defines.WS_MINIMIZE):  # if minimized
            ShowWindow(window.wrapper_object(), 9)  # restore window state
        else:
            SetForegroundWindow(window.wrapper_object())  # bring to front

    def handle(self, title):
        if any(s in title for s in {"提示信息", "委托确认", "网上交易用户协议", "撤单确认"}):
            self._submit_by_shortcut()
            return None

        if "提示" in title:
            content = self._extract_content()
            self._submit_by_click()
            return {"message": content}

        content = self._extract_content()
        self._close()
        return {"message": "unknown message: {}".format(content)}

    def _extract_content(self):
        return self._app.top_window().Static.window_text()

    @staticmethod
    def _extract_entrust_id(content):
        return re.search(r"[\da-zA-Z]+", content).group()

    def _submit_by_click(self):
        try:
            self._app.top_window()["确定"].click()
        except Exception as ex:
            self._app.Window_(best_match="Dialog", top_level_only=True).ChildWindow(
                best_match="确定"
            ).click()

    def _submit_by_shortcut(self):
        self._set_foreground(self._app.top_window())
        self._app.top_window().type_keys("%Y", set_foreground=False)

    def _close(self):
        self._app.top_window().close()


class TradePopDialogHandler(PopDialogHandler):
    def handle(self, title) -> Optional[dict]:
        if title == "委托确认":
            self._submit_by_shortcut()
            return None

        if title == "提示信息":
            content = self._extract_content()
            if "超出涨跌停" in content:
                self._submit_by_shortcut()
                return None

            if "委托价格的小数价格应为" in content:
                self._submit_by_shortcut()
                return None

            if "逆回购" in content:
                self._submit_by_shortcut()
                return None

            if "正回购" in content:
                self._submit_by_shortcut()
                return None

            return None

        if title == "提示":
            content = self._extract_content()
            if "成功" in content:
                entrust_no = self._extract_entrust_id(content)
                self._submit_by_click()
                return {"entrust_no": entrust_no}

            self._submit_by_click()
            time.sleep(0.05)
            raise TradeError(content)
        self._close()
        return None


class BaseTrader(abc.ABC):
    def __init__(self):
        pass

    def connect(self, exe_path: str):
        pass

    def buy(self, stock_id: str, price, amount):
        pass


class THSTrader(BaseTrader):
    def __init__(self, exe_path):
        super().__init__()
        self.connect(exe_path)

    def connect(self, exe_path: str):
        self._app = pywinauto.Application().connect(path=exe_path, timeout=10)
        self._close_prompt_windows()
        self._main = self._app.top_window()
        self._init_toolbar()

    def _close_prompt_windows(self):
        self.wait(1)
        for window in self._app.windows(class_name="#32770", visible_only=True):
            title = window.window_text()
            if title != config.TITLE:
                logger.info("close " + title)
                window.close()
                self.wait(0.2)
        self.wait(1)

    def wait(self, seconds):
        time.sleep(seconds)

    def _init_toolbar(self):
        self._toolbar = self._main.child_window(class_name="ToolbarWindow32")

    def buy(self, security, price, amount, **kwargs):
        self._switch_left_menus(["买入[F1]"])

        return self.trade(security, price, amount)

    def _switch_left_menus(self, path, sleep=0.2):
        self._get_left_menus_handle().get_item(path).click()
        self.wait(sleep)

    @functools.lru_cache()
    def _get_left_menus_handle(self):
        count = 2
        while True:
            try:
                handle = self._main.child_window(
                    control_id=129, class_name="SysTreeView32"
                )
                if count <= 0:
                    return handle
                # sometime can't find handle ready, must retry
                handle.wait("ready", 2)
                return handle
            # pylint: disable=broad-except
            except Exception as ex:
                logger.exception("error occurred when trying to get left menus")
            count = count - 1

    def trade(self, security, price, amount):
        self._set_trade_params(security, price, amount)

        self._submit_trade()

        return self._handle_pop_dialogs(
            handler_class=TradePopDialogHandler
        )

    def _set_trade_params(self, security, price, amount):
        code = security[-6:]

        self._type_edit_control_keys(config.TRADE_SECURITY_CONTROL_ID, code)

        # wait security input finish
        self.wait(0.1)

        self._type_edit_control_keys(
            config.TRADE_PRICE_CONTROL_ID,
            round_price_by_code(price, code),
        )
        self._type_edit_control_keys(
            config.TRADE_AMOUNT_CONTROL_ID, str(int(amount))
        )

    def _type_edit_control_keys(self, control_id, text):
        editor = self._main.child_window(control_id=control_id, class_name="Edit")
        editor.select()
        editor.type_keys(text)

    def _submit_trade(self):
        time.sleep(0.2)
        self._main.child_window(
            control_id=config.TRADE_SUBMIT_CONTROL_ID, class_name="Button"
        ).click()

    def _handle_pop_dialogs(self, handler_class=PopDialogHandler):
        handler = handler_class(self._app)

        while self.is_exist_pop_dialog():
            try:
                title = self._get_pop_dialog_title()
            except pywinauto.findwindows.ElementNotFoundError:
                return {"message": "success"}

            result = handler.handle(title)
            if result:
                return result
        return {"message": "success"}

    def is_exist_pop_dialog(self):
        self.wait(0.5)  # wait dialog display
        try:
            return (
                    self._main.wrapper_object() != self._app.top_window().wrapper_object()
            )
        except (
                findwindows.ElementNotFoundError,
                timings.TimeoutError,
                RuntimeError,
        ) as ex:
            logger.exception("check pop dialog timeout")
            return False

    def _get_pop_dialog_title(self):
        return (
            self._app.top_window()
                .child_window(control_id=config.POP_DIALOD_TITLE_CONTROL_ID)
                .window_text()
        )
