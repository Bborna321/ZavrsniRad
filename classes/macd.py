import mplfinance as mpf
from classes.components.datamanager import GetData
import global_vars as gv


class Macd:
    def __init__(self, ival, ax1):
        self.ival = ival
        self.ax1 = ax1
        self.data = GetData()[2:]
        self.close_prices = self.data['close']

        self.mean12 = self.close_prices.ewm(span=12).mean()
        self.mean26 = self.close_prices.ewm(span=26).mean()

        self.macd = self.mean12-self.mean26
        self.signal_line = self.macd.ewm(span=9).mean()

        self.histogram = self.macd-self.signal_line


    def GetAnimationData(self):
        self.data['Signal'] = self.signal_line
        self.data['Macd'] = self.macd
        self.data['Histogram'] = self.histogram
        self.data['Mean12'] = self.mean12
        self.data['Mean26'] = self.mean26

        self.ap = [
            mpf.make_addplot(self.data['Signal'].iloc[0:self.ival], type='line', ax=self.ax1),
            mpf.make_addplot(self.data['Macd'].iloc[0:self.ival], type='line', ax=self.ax1),
            mpf.make_addplot(self.data['Mean26'].iloc[0:self.ival], type='line', ax=self.ax1),
            mpf.make_addplot(self.data['Mean12'].iloc[0:self.ival], type='line', ax=self.ax1),
            mpf.make_addplot(self.data['Histogram'].iloc[0:self.ival], type='bar', ax=self.ax1,color=gv.darkColor)
        ]

        return self.data,self.ap,self.ax1

