from classes.components.datamanager import *
import numpy as np


class RSI:
    def __init__(self, ax1):
        self.ax1 = ax1
        self.data = GetData()
        self.GetRSI()

    def GetRSI(self):
        ret = self.data['close'].diff()
        up = []
        down = []
        for i in range(len(ret)):
            if ret[i] == np.nan:
                ret[i] = 0.0

            if ret[i] < 0:
                up.append(0)
                down.append(ret[i])
            else:
                up.append(ret[i])
                down.append(0)
        upSeries = pd.Series(up)
        downSeries = pd.Series(down).abs()
        upEWM = upSeries.ewm(com=14 - 1, adjust=False).mean()
        downEWM = downSeries.ewm(com=14 - 1, adjust=False).mean()
        rs = upEWM / downEWM
        rsi = 100 - (100 / (1 + rs))
        rsiDF = pd.DataFrame(rsi).rename(columns={0: 'rsi'}).set_index(self.data['close'].index)
        rsiDF['rsi'] = rsiDF['rsi'].fillna(0)
        self.data['RSI'] = list(rsiDF['rsi'].values)

    def GetAnimationData(self, leftValue, rightValue, ax1, ax2):
        """print("data---------------------\n",self.data)
        print("ap-----------------------\n", self.ap)
        print("ax1----------------------\n", self.ax1)"""

        ap = [[self.data['RSI'].iloc[leftValue: rightValue], 'line', 1, ax2]]
        return ap

    def UpdateData(self, newData):
        n = len(list(newData['close'].values))
        newData['RSI'] = [""] * n
        self.data = pd.concat([self.data, newData], axis=0)
        self.GetRSI()
