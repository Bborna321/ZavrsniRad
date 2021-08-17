from classes.components import settings
from global_vars import *
from tkinter import *
from classes.components.menubar import popupmsg


class Money_manager:
    def __init__(self, curr_mon, sell_high, sell_low, mylist):
        self.current_money = curr_mon
        self.mylist = mylist
        self.sell_high = sell_high
        self.sell_low = sell_low
        self.in_trading = False

    def money_update(self, old_price, new_price):
        if self.in_trading:
            self.current_money *= new_price / old_price

        if self.current_money <= self.sell_low:
            # popupmsg("Stop Trading1")
            self.in_trading = False
        elif self.current_money >= self.sell_high:
            # popupmsg("Stop Trading2")
            self.in_trading = False

    def automatic_buy_sell_when_price_is_high_low(self, new_price, old_price, high_candle, low_candle):
        if not self.in_trading:
            return

        dummy_money_high = self.current_money * high_candle / old_price
        dummy_money_low = self.current_money * high_candle / old_price

        if dummy_money_high >= self.sell_high:
            self.current_money = self.sell_high * 1.0055
            # popupmsg("Stop Trading3")
            self.in_trading = False

        elif dummy_money_low <= self.sell_low:
            self.current_money = self.sell_low * 0.9946
            # popupmsg("Stop Trading4")
            self.in_trading = False

    def trader(self, new_price, old_price, high_candle, low_candle):
        if not self.in_trading:
            return
        self.automatic_buy_sell_when_price_is_high_low(new_price, old_price, high_candle, low_candle)
        self.money_update(new_price, old_price)

        text = [
            "\n current money " + str(round(self.current_money, 2)),
            "\n trading status: " + str(self.in_trading)
        ]
        settings.Log(self.mylist, text)
