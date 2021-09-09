import mplfinance as mpf
from classes.components.datamanager import GetData
import globalvars as gv
import pandas as pd


class Macd:
    def __init__(self, ax1):
        self.ax1 = ax1
        self.data = GetData()
        self.dates = self.data['date']
        self.__SetMeans()

    def __SetMeans(self):
        self.closePrices = self.data['close']
        self.mean12 = self.closePrices.ewm(span=12, adjust=False).mean()
        self.mean26 = self.closePrices.ewm(span=26, adjust=False).mean()

        self.macd = self.mean12 - self.mean26
        self.signalLine = self.macd.ewm(span=9, adjust=False).mean()

        self.histogram = self.macd - self.signalLine
        # self.

    def TradingStopSignal(self, ival):
        ival = ival-1
        if self.histogram[ival] > 0 and self.histogram[ival - 1] > 0 \
                and self.histogram[ival] < self.histogram[ival - 1] > 0:
            return True
        if self.histogram[ival] <= 0:
            return True
        return False

    def TradingStartSignal(self, ival):
        ival = ival-1
        return self.histogram[ival - 1] < 0 and self.histogram[ival] > 0

    def GetAnimationData(self, leftValue, rightValue, ax1, ax2):
        self.data['Signal'] = self.signalLine
        self.data['Macd'] = self.macd
        self.data['Histogram'] = self.histogram
        self.data['Mean12'] = self.mean12
        self.data['Mean26'] = self.mean26

        colors = ['g' if v >= 0 else 'r' for v in self.data["Histogram"].iloc[leftValue: rightValue]]
        self.ap = [
            [self.data['Signal'].iloc[leftValue: rightValue], 'line', 1, ax2],
            [self.data['Macd'].iloc[leftValue: rightValue], 'line', 1, ax2],
            [self.data['Mean26'].iloc[leftValue: rightValue], 'line', 0, ax1],
            [self.data['Mean12'].iloc[leftValue: rightValue], 'line', 0, ax1],
            [self.data['Histogram'].iloc[leftValue: rightValue], 'bar', 1, ax2, colors]
        ]
        return self.ap

    def UpdateData(self, newData):
        n = len(list(newData['close'].values))
        newData['Signal'] = [""] * n
        newData['Macd'] = [""] * n
        newData['Histogram'] = [""] * n
        newData['Mean12'] = [""] * n
        newData['Mean26'] = [""] * n
        self.data = pd.concat([self.data, newData], axis=0)
        self.__SetMeans()
