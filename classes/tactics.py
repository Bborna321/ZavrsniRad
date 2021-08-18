from classes.RSI import RSI
from classes.FibonacciRetracement import FibonacciRetracement
from classes.BollingerBands import BollingerBands
from classes.macd import Macd
from classes.components.datamanager import GetData
import mplfinance as mpf
import pandas as pd


class Tactics:
    def __init__(self, ax1, mylist, options, money_manager):
        self.ival = 20
        self.ax1 = ax1
        self.data = GetData()
        self.rsi = RSI(ax1)
        self.fibo = FibonacciRetracement(ax1, 50)
        self.boll = BollingerBands(ax1)
        self.macd = Macd(ax1)
        # self.money_manager = money_manager
        self.options = options

    def faj(self, options, money_manager):

        if self.macd.trading_start_signal(self.ival):
            print("ulazim u trade")
            options.enter_trade(money_manager)
        if self.macd.trading_stop_signal(self.ival):
            print("izlazim iz tradea")
            options.exit_trade(money_manager)

    def LoadMoreData(self):
        print("ovdje")
        newData = GetData()
        self.data = pd.concat([self.data, newData], axis=0)
        self.fibo.UpdateData(newData)
        self.macd.UpdateData(newData)
        self.boll.UpdateData(newData)
        self.rsi.UpdateData(newData)

    def GetAnimationData(self, leftValue, rightValue, toAnimate):
        ap = []
        temp = []
        if toAnimate[0] == 1:
            temp = temp + self.macd.GetAnimationData(leftValue, rightValue)
        if toAnimate[1] == 1:
            temp = temp + self.boll.GetAnimationData(leftValue, rightValue)
        if toAnimate[2] == 1:
            temp = temp + self.fibo.GetAnimationData(leftValue, rightValue)
        if toAnimate[3] == 1:
            temp = temp + self.rsi.GetAnimationData(leftValue, rightValue)

        for t in temp:
            ap.append(mpf.make_addplot(t[0], type=t[1], ax=self.ax1))

        return ap, self.ax1
