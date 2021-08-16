import global_vars as gv


class Money_manager:
    def __init__(self,curr_mon,sell_high,sell_low):
        self.current_money = curr_mon
        self.sell_high = sell_high
        self.sell_low = sell_low
        self.in_trading = True

    def money_update(self,old_price,new_price):
        if self.in_trading:
            self.current_money *= new_price/old_price

        if self.current_money <= self.sell_low:
            self.in_trading = False
        elif self.current_money >= self.sell_high:
            self.in_trading = False


    def automatic_buy_sell_when_price_is_high_low(self,new_price,old_price,high_candle,low_candle):
        if not self.in_trading:
            return

        dummy_money_high = self.current_money * high_candle/old_price
        dummy_money_low = self.current_money * high_candle / old_price

        if dummy_money_high >= self.sell_high:
            self.current_money = self.sell_high*1.0055
            self.in_trading = False

        elif dummy_money_low <= self.sell_low:
            self.current_money = self.sell_low*0.9946
            self.in_trading = False

