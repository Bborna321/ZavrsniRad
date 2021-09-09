from classes.components.datamanager import Log
import classes.components.datamanager as datamanager


class MoneyManager:
    def __init__(self, currMon, sellHigh, sellLow, mylist):
        self.mylist = mylist
        self.currentMoney = currMon
        self.sellHigh = sellHigh
        self.sellLow = sellLow
        self.inTrading = False
        self.pushLatestEnterDate = False
        self.pushLatestExitDate = False
        self.tradingStarts = []
        self.tradingStops = []
        self.amIAllowedToEnterTrade = True
        self.amIAllowedToExitTrade = True
        self.autoEnter = True

    def MoneyUpdate(self, oldPrice, newPrice, potentialDate, options):
        if self.inTrading:
            self.currentMoney *= newPrice / oldPrice

            if self.currentMoney <= self.sellLow and self.autoEnter:
                options.ExitTrade(self)
            elif self.currentMoney >= self.sellHigh and self.autoEnter:
                options.ExitTrade(self)

    # def automatic_buy_sell_when_price_is_high_low(self, newPrice, oldPrice, high_candle, low_candle):
    #     if not self.inTrading:
    #         return
    #
    #     dummy_money_high = self.currentMoney * high_candle / oldPrice
    #     dummy_money_low = self.currentMoney * low_candle / oldPrice
    #
    #     if dummy_money_high >= self.sellHigh:
    #         self.currentMoney = self.sellHigh * 1.0055
    #         # popupmsg("Stop Trading3")
    #         self.inTrading = False
    #
    #     elif dummy_money_low <= self.sellLow:
    #         self.currentMoney = self.sellLow * 0.9946
    #         # popupmsg("Stop Trading4")
    #         self.inTrading = False

    def UpdateSellHighSellLow(self):
        updateJson = datamanager.GetJsonData('data_money.json')
        self.sellHigh = self.currentMoney * float(updateJson['sell_high'])
        self.sellLow = self.currentMoney * float(updateJson['sell_low'])

        datamanager.CreateJsonMoney(self.currentMoney, float(updateJson['sell_high']), float(updateJson['sell_low']))

    def Trader(self, newPrice, oldPrice, high_candle, low_candle, potentialDate, options):
        if self.pushLatestEnterDate == True:
            self.tradingStarts.append(potentialDate)
            self.pushLatestEnterDate = False
        elif self.pushLatestExitDate == True:
            self.tradingStops.append(potentialDate)
            self.pushLatestExitDate = False
        if not self.inTrading:
            return
        # self.automatic_buy_sell_when_price_is_high_low(newPrice, oldPrice, high_candle, low_candle)
        self.MoneyUpdate(newPrice, oldPrice, potentialDate, options)

    def EnterTrade(self):
        if len(self.tradingStarts) > len(self.tradingStops):
            return False
        newlyEntered = False
        if self.inTrading == True:
            self.pushLatestEnterDate = False
        else:
            self.pushLatestEnterDate = True
            newlyEntered = True
        self.inTrading = True
        self.UpdateSellHighSellLow()

        # print("startovi tradea:",self.tradingStarts)

        return newlyEntered

    def ExitTrade(self):
        newlyExited = False
        if self.inTrading == False:
            self.pushLatestExitDate = False
        else:
            self.pushLatestExitDate = True
            newlyExited = True
        self.inTrading = False

        # print("stopovi tradea:", self.tradingStops)

        return newlyExited

    def ChangeAutoTrade(self, flag):
        self.autoEnter = flag
