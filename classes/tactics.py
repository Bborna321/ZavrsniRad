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

    def MACDTrader(self, options, moneyManager):
        if self.macd.TradingStartSignal(self.ival) and not moneyManager.inTrading:
            options.EnterTrade(moneyManager)
        if self.macd.TradingStopSignal(self.ival) and moneyManager.inTrading:
            options.ExitTrade(moneyManager)

    def FIBOTrader(self, options, moneyManager, plotdata, leftValue, rightValue):
        self.fibo.SetData(leftValue, rightValue)
        if self.fibo.TradingStartSignal(self.ival, moneyManager) and not moneyManager.inTrading:
            options.EnterTrade(moneyManager)
        if self.fibo.TradingStopSignal(self.ival, plotdata) and moneyManager.inTrading:
            options.ExitTrade(moneyManager)

    def BollRSITrader(self, options, moneyManager, leftValue, rightValue):
        rsiData = self.rsi.data
        if rsiData['RSI'][rightValue-1] <= 25 and not moneyManager.inTrading and \
                self.data['close'][rightValue-1] <= self.boll.lowerBound[rightValue-1]:
            options.EnterTrade(moneyManager)
        if rsiData['RSI'][rightValue-1] >= 75 and moneyManager.inTrading and \
                self.data['close'][rightValue-1] >= self.boll.upperBound[rightValue-1]:
            options.ExitTrade(moneyManager)


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
            if len(t) == 5:
                print("tu")
                ap.append(mpf.make_addplot(t[0], type=t[1], ax=t[3], panel=t[2], color=t[4]))
            else:
                ap.append(mpf.make_addplot(t[0], type=t[1], ax=t[3], panel=t[2]))

        return ap, self.ax1, self.ax2
