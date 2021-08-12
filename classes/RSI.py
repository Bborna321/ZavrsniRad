from classes.components.datamanager import *
import mplfinance as mpf
import numpy as np

class RSI:
    def __init__(self, ival, ax1):
        self.ival = ival
        self.ax1 = ax1
        self.data = GetData()
        self.get_rsi()


    def get_rsi(self):
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
        up_series = pd.Series(up)
        down_series = pd.Series(down).abs()
        up_ewm = up_series.ewm(com=14 - 1, adjust=False).mean()
        down_ewm = down_series.ewm(com=14 - 1, adjust=False).mean()
        rs = up_ewm / down_ewm
        rsi = 100 - (100 / (1 + rs))
        rsi_df = pd.DataFrame(rsi).rename(columns={0: 'rsi'}).set_index(self.data['close'].index)
        rsi_df['rsi'] = rsi_df['rsi'].fillna(0)
        self.data['RSI'] = list(rsi_df['rsi'].values)

        self.__SetAnimationData()

    def __SetAnimationData(self):
        self.ap = mpf.make_addplot(self.data['RSI'].iloc[0:self.ival], type='line', ax=self.ax1)

    def GetAnimationData(self):
        return self.data, self.ap, self.ax1

