from classes.RSI import RSI
from classes.FibonacciRetracement import FibonacciRetracement
from classes.BollingerBands import BollingerBands
from classes.macd import Macd
from classes.components.datamanager import GetData
import mplfinance as mpf
import pandas as pd


class Tactics:
    def __init__(self, ax1, ax2, options):
        self.ival = 20
        self.ax1 = ax1
        self.ax2 = ax2
        self.data = GetData()
        self.rsi = RSI(ax1)
        self.fibo = FibonacciRetracement(100)
        self.boll = BollingerBands(ax1)
        self.macd = Macd(ax1)
        self.options = options
        """potencijalno možda ne dobra ideja
        jer se tako stvara novi self.options
        kojemu promjene ne idu na isti način
        kao i u prosljeđenom optionsu,
        no možda nije bitno za ovo"""

    def MACDTrader(self, options, money_manager):
        if self.macd.trading_start_signal(self.ival) and not money_manager.in_trading:
            options.enter_trade(money_manager)
        if self.macd.trading_stop_signal(self.ival) and money_manager.in_trading:
            options.exit_trade(money_manager)

    def FIBOTrader(self, options, money_manager, plotdata, leftValue, rightValue):
        self.fibo.SetData(leftValue, rightValue)
        if self.fibo.trading_start_signal(self.ival, money_manager) and not money_manager.in_trading:
            options.enter_trade(money_manager)
        if self.fibo.trading_stop_signal(self.ival, plotdata) and money_manager.in_trading:
            options.exit_trade(money_manager)

    def BollRSITrader(self, options, money_manager, leftValue, rightValue):
        rsiData = self.rsi.data
        if rsiData['RSI'][rightValue-1] <= 25 and not money_manager.in_trading and \
                self.data['close'][rightValue-1] <= self.boll.lowerBound[rightValue-1]:
            options.enter_trade(money_manager)
        if rsiData['RSI'][rightValue-1] >= 75 and money_manager.in_trading and \
                self.data['close'][rightValue-1] >= self.boll.upperBound[rightValue-1]:
            options.exit_trade(money_manager)


    def LoadMoreData(self):
        newData = GetData()
        if newData['close'].values.shape[0] == 0:
            return True
        self.data = pd.concat([self.data, newData], axis=0)
        self.fibo.UpdateData(newData)
        self.macd.UpdateData(newData)
        self.boll.UpdateData(newData)
        self.rsi.UpdateData(newData)
        return False

    def GetAnimationData(self, leftValue, rightValue, toAnimate):
        ap = []
        temp = []
        if toAnimate[0] == 1:
            temp = temp + self.macd.GetAnimationData(leftValue, rightValue, self.ax1, self.ax2)
        if toAnimate[1] == 1:
            temp = temp + self.boll.GetAnimationData(leftValue, rightValue, self.ax1, self.ax2)
        if toAnimate[2] == 1:
            temp = temp + self.fibo.GetAnimationData(leftValue, rightValue, self.ax1, self.ax2)
        if toAnimate[3] == 1:
            temp = temp + self.rsi.GetAnimationData(leftValue, rightValue, self.ax1, self.ax2)

        for t in temp:
            ap.append(mpf.make_addplot(t[0], type=t[1], ax=t[3], panel=t[2]))

        return ap, self.ax1, self.ax2
