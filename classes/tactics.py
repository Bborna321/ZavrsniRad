from classes.RSI import RSI
from classes.FibonacciRetracement import FibonacciRetracement
from classes.BollingerBands import BollingerBands
from classes.macd import Macd
from classes.components.datamanager import GetData
import mplfinance as mpf
import classes.money_manager
import global_vars as gv

class Tactics:
    def __init__(self, ax1, mylist):
        self.ival = 0
        self.ax1 = ax1
        self.data = GetData()
        self.rsi = RSI(ax1)
        self.fibo = FibonacciRetracement(ax1)
        self.boll = BollingerBands(ax1)
        self.macd = Macd(ax1)
        self.Money_manager = classes.money_manager.Money_manager(gv.current_money,gv.sell_at_high,gv.sell_at_low, mylist)

    def GetAnimationData(self, ival, toAnimate):
        ap = []
        temp = []
        if(toAnimate[0] == 1):
            temp = temp + self.macd.GetAnimationData(ival)
        if (toAnimate[1] == 1):
            temp = temp + self.boll.GetAnimationData(ival)
        if (toAnimate[2] == 1):
            temp = temp + self.fibo.GetAnimationData(ival)
        if (toAnimate[3] == 1):
            temp = temp + self.rsi.GetAnimationData(ival)

        for t in temp:
            ap.append(mpf.make_addplot(t[0], type=t[1], ax=self.ax1))

        return self.data, ap, self.ax1
