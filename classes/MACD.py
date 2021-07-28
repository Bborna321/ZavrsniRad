from classes.BaseTactic import BaseTactic

class MACD(BaseTactic):
    def __init__(self, data, period):
        BaseTactic.__init__(self, data, period)
        self.buySignals = []
        self.EMA12 = []
        self.EMA26 = []
        self.MACDline = []

    def CalculateMovingAverage(self, movingAverage, data = None):
        self.ChangePeriod(12)
        self.EMA12 = BaseTactic.CalculateMovingAverage(self, "EMA", data)

        self.ClearMovingAverages()
        self.ChangePeriod(26)
        self.EMA26 = BaseTactic.CalculateMovingAverage(self, "EMA", data)

        self.MACDline = list(map(lambda x, y: round(x - y,4), self.EMA12, self.EMA26))
        self.ChangePeriod(9)
        self.signalLine = BaseTactic.CalculateMovingAverage(self, "EMA", self.MACDline)
