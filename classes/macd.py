import mplfinance as mpf
from classes.components.datamanager import GetData
import global_vars as gv


class Macd:
    def __init__(self, ax1):
        self.ax1 = ax1
        self.data = GetData()[2:]
        self.close_prices = self.data['close']

        self.mean12 = self.close_prices.ewm(span=12,adjust=False).mean()
        self.mean26 = self.close_prices.ewm(span=26,adjust=False).mean()

        self.macd = self.mean12-self.mean26
        self.signal_line = self.macd.ewm(span=9,adjust=False).mean()

        self.histogram = self.macd-self.signal_line


    def GetAnimationData(self,ival):
        self.data['Signal'] = self.signal_line
        self.data['Macd'] = self.macd
        self.data['Histogram'] = self.histogram
        self.data['Mean12'] = self.mean12
        self.data['Mean26'] = self.mean26

        self.ap = [
            [self.data['Signal'].iloc[0:ival], 'line'],
            [self.data['Macd'].iloc[0:ival], 'line'],
            [self.data['Mean26'].iloc[0:ival],  'line'],
            [self.data['Mean12'].iloc[0:ival], 'line'],
            [self.data['Histogram'].iloc[0:ival], 'bar']
        ]

        return self.ap

