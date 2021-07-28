from classes.BaseTactic import BaseTactic

class MACD(BaseTactic):
    def __init__(self, data, period):
        BaseTactic.__init__(self, data, period)
        self.EMA12 = []
        self.EMA26 = []
        self.subtracted = []


    def CalculateMovingAverage(self):
        self.ChangePeriod(12)
        BaseTactic.CalculateMovingAverage(self, "EMA")
        self.EMA12 = self.ExponentialMovingAverage

        self.ClearMovingAverages()
        self.ChangePeriod(26)
        BaseTactic.CalculateMovingAverage(self, "EMA")
        self.EMA26 = self.ExponentialMovingAverage

        self.subtracted = list(map(lambda x, y: x - y, self.EMA12, self.EMA26))
