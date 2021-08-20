import mplfinance as mpf
from classes.components.datamanager import GetData
import global_vars as gv
import pandas as pd


class Macd:
    def __init__(self, ax1):
        self.ax1 = ax1
        self.data = GetData()
        self.dates = self.data['date']
        self.__SetMeans()

    def __SetMeans(self):
        self.close_prices = self.data['close']
        self.mean12 = self.close_prices.ewm(span=12, adjust=False).mean()
        self.mean26 = self.close_prices.ewm(span=26, adjust=False).mean()

        self.macd = self.mean12 - self.mean26
        self.signal_line = self.macd.ewm(span=9, adjust=False).mean()

        self.histogram = self.macd - self.signal_line
        # self.

    def trading_stop_signal(self, ival):
        if self.histogram[ival] > 0 and self.histogram[ival - 1] > 0 \
                and self.histogram[ival] < self.histogram[ival - 1] > 0:
            return True
        if self.histogram[ival] <= 0:
            return True
        return False

    def trading_start_signal(self, ival):
        return self.histogram[ival - 1] < 0 and self.histogram[ival] > 0

    def GetAnimationData(self, leftValue, rightValue):
        self.data['Signal'] = self.signal_line
        self.data['Macd'] = self.macd
        self.data['Histogram'] = self.histogram
        self.data['Mean12'] = self.mean12
        self.data['Mean26'] = self.mean26

        self.ap = [
            # [self.data['Signal'].iloc[leftValue: rightValue], 'line'],
            # [self.data['Macd'].iloc[leftValue: rightValue], 'line'],
            [self.data['Mean26'].iloc[leftValue: rightValue], 'line'],
            [self.data['Mean12'].iloc[leftValue: rightValue], 'line'],
            [self.data['Histogram'].iloc[leftValue: rightValue], 'bar']
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
