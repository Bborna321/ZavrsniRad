import statistics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mplfinance as mpf
from classes.components.datamanager import GetData
import global_vars as gv
from math import sqrt


class BollingerBands:
    def __init__(self, ival, ax1):
        self.ival = ival
        self.ax1 = ax1
        self.data = GetData()[2:]
        self.close_prices = self.data['close']
        self.ema20 = self.close_prices.ewm(span=20).mean()
        self.std = []

        for x in self.close_prices.ewm(span=20).std()[0:20]:
            self.std.append(x*2)
        self.std_close_ema20()

    def std_close_ema20(self):
        diff_sq = []

        for i in range(len(self.close_prices)):

            diff = self.close_prices[i]-self.ema20[i]
            diff_sq.append((diff*diff))

            if i >= 20:
                self.std.append(2*sqrt(sum(diff_sq[-21:-1])/20))

        plt.plot( np.arange(len(self.data)),self.close_prices          )
        plt.plot(np.arange(len(self.data)), self.ema20)
        plt.plot(np.arange(len(self.data)), self.ema20+self.std,color=gv.darkColor)
        plt.plot(np.arange(len(self.data)), self.ema20- self.std,color=gv.darkColor)

        self.upperBound = self.ema20+self.std
        self.lowerBound = self.ema20-self.std

    def __SetAnimationData(self):
        pass

    def GetAnimationData(self):
        self.data['Upper bound'] = self.upperBound
        self.data['Lower bound'] = self.lowerBound
        self.ap = [
            mpf.make_addplot(self.data['Upper Bound'].iloc[0:self.ival], type='line', ax=self.ax1),
            mpf.make_addplot(self.data['Lower Bound'].iloc[0:self.ival], type='line', ax=self.ax1),
        ]
        return self.data,self.ap,self.ax1