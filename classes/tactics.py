from classes.RSI import RSI
from classes.FibonacciRetracement import FibonacciRetracement
from classes.BollingerBands import BollingerBands
from classes.macd import Macd
from classes.components.datamanager import GetData
import mplfinance as mpf

class Tactics:
    def __init__(self, ax1):
        self.ax1 = ax1
        self.data = GetData()
        self.rsi = RSI(ax1)
        self.fibo = FibonacciRetracement(ax1)
        self.boll = BollingerBands(ax1)
        self.macd = Macd(ax1)

    def GetAnimationData(self, ival):
        a, tempAp, b = self.macd.GetAnimationData(ival)
        c, tempAp1, d = self.rsi.GetAnimationData(ival)
        ap = []
        for temp in tempAp:
            ap.append(mpf.make_addplot(temp[0], type=temp[1], ax=self.ax1))
        return a, ap, b
