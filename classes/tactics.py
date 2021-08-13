from classes.RSI import RSI
from classes.FibonacciRetracement import FibonacciRetracement
from classes.components.datamanager import GetData


class Tactics:
    def __init__(self, ival, ax1):
        self.ival = ival
        self.ax1 = ax1
        self.data = GetData()
        self.rsi = RSI(ival, ax1)
        self.fibo = FibonacciRetracement(ival, ax1)
        self.__GetTactics()

    def __GetTactics(self):
        self.ap = self.fibo.ap
        self.ap.append(self.rsi.ap)
        self.data['Maximum price'] = list(self.fibo.data['Maximum price'].values)
        self.data['Fourth level'] = list(self.fibo.data['Fourth level'].values)
        self.data['Third level'] = list(self.fibo.data['Third level'].values)
        self.data['Second level'] = list(self.fibo.data['Second level'].values)
        self.data['First level'] = list(self.fibo.data['First level'].values)
        self.data['Minimum price'] = list(self.fibo.data['Minimum price'].values)
        self.data['RSI'] = list(self.rsi.data['RSI'].values)

    def GetAnimationData(self):
        return self.data, self.ap, self.ax1
