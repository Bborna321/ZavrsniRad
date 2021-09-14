from classes.components.datamanager import GetData
from math import sqrt
import pandas as pd

class BollingerBands:
    def __init__(self, ax1):
        self.ax1 = ax1
        self.data = GetData()
        self.__SetBounds()

    def __SetBounds(self):
        self.closePrices = self.data['close']
        self.ema20 = self.closePrices.ewm(span=20).mean()
        self.std = []

        for x in self.closePrices.ewm(span=20).std()[0:20]:
            self.std.append(x * 2)

        self.upperBound, self.lowerBound = self.STDCloseEMA20()
        #print(self.upperBound, self.lowerBound)

    def STDCloseEMA20(self):
        diffSQ = []

        for i in range(len(self.closePrices)):

            diff = self.closePrices[i] - self.ema20[i]
            diffSQ.append((diff * diff))

            if i >= 20:
                self.std.append(2 * sqrt(sum(diffSQ[-21:-1]) / 20))

        return self.ema20 + self.std, self.ema20 - self.std

    def __SetAnimationData(self):
        pass

    def GetAnimationData(self, leftValue, rightValue, ax1, ax2):
        self.data['Upper bound'] = self.upperBound
        self.data['Lower bound'] = self.lowerBound
        self.ap = [
            [self.data['Upper bound'].iloc[leftValue: rightValue], 'line', 0, ax1],
            [self.data['Lower bound'].iloc[leftValue: rightValue], 'line', 0, ax1]
        ]
        return self.ap

    def UpdateData(self, newData):
        n = len(list(newData['close'].values))
        newData['Upper bound'] = [""] * n
        newData['Lower bound'] = [""] * n
        self.data = pd.concat([self.data, newData], axis=0)
        self.__SetBounds()
