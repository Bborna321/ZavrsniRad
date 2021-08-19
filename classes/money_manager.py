from classes.components.datamanager import Log
import classes.components.datamanager as datamanager


class Money_manager:
    def __init__(self, curr_mon, sell_high, sell_low, mylist):
        self.mylist = mylist
        self.current_money = curr_mon
        self.sell_high = sell_high
        self.sell_low = sell_low
        self.in_trading = False
        self.push_latest_enter_date = False
        self.push_latest_exit_date = False
        self.trading_starts = []
        self.trading_stops = []

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

    def update_sell_high_sell_Low(self):
        updateJson = datamanager.GetJsonData('data_money.json')
        self.sell_high = self.current_money * float(updateJson['sell_high'])
        self.sell_low = self.current_money * float(updateJson['sell_low'])

        datamanager.CreateJsonMoney(self.current_money, float(updateJson['sell_high']), float(updateJson['sell_low']))

    def trader(self, new_price, old_price, high_candle, low_candle, potentialDate):
        if self.push_latest_enter_date == True:
            self.trading_starts.append(potentialDate)
            self.push_latest_enter_date = False
        elif self.push_latest_exit_date == True:
            self.trading_stops.append(potentialDate)
            self.push_latest_exit_date = False
        if not self.in_trading:
            return
        self.automatic_buy_sell_when_price_is_high_low(new_price, old_price, high_candle, low_candle)
        self.money_update(new_price, old_price)

        text = [
            "\n current money " + str(round(self.current_money, 2)),
            "\n trading status: " + str(self.in_trading)
        ]
        Log(self.mylist, text)

    def enter_trade(self):
        if self.in_trading == True:
            self.push_latest_enter_date = False
        else:
            self.push_latest_enter_date = True
        self.in_trading = True
        self.update_sell_high_sell_Low()

        print("startovi tradea:",self.trading_starts)

    def exit_trade(self):

        if self.in_trading == False:
            self.push_latest_exit_date = False
        else:
            self.push_latest_exit_date = True
        self.in_trading = False

        print("stopovi tradea:", self.trading_stops)
