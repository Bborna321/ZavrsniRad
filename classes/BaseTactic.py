class BaseTactic:
    def __init__(self, data, period):
        self.data = data
        self.period = period
        self.day = 0
        self.SimpleMovingAverage = []
        self.ExponentialMovingAverage = []

    def CalculateMovingAverage(self, movingAverage):
        if(movingAverage == "SMA"):
            self.CalculateSimpleAverage()
        else:
            self.CalculateExponentialAverage(len(self.data)-1)

    # Simple moving average formula:
    # SMA = period sum / N
    # N = number of days in a given period
    # period sum = sum of stocks closing prices in that period
    def CalculateSimpleAverage(self):
        i = 0
        while (len(self.data) - (self.period + i)) >= 0:
            movingAverage = self.data[len(self.data) - (self.period + i): len(self.data)-i]
            self.SimpleMovingAverage.append(sum(movingAverage) / self.period)
            i = i + 1

        self.SimpleMovingAverage.reverse()


    # Exponential moving average formula:
    # S(t) = a*Y_t + (1-a)*S_{t-1} , t > 1
    # S(t) = Y_t , t = 1
    def CalculateExponentialAverage(self, position):
        k = 2 / (self.period + 1)
        if position == 0:
            self.ExponentialMovingAverage.append(self.data[0])
            return self.data[0]
        else:
            self.CalculateExponentialAverage(position - 1)
            previous = self.ExponentialMovingAverage[position - 1]
            self.ExponentialMovingAverage.append(k*self.data[position] + (1.0 - k)*previous)
            return 0

    def ClearMovingAverages(self):
        self.ExponentialMovingAverage = []
        self.SimpleMovingAverage = []
        self.day = 0

    def ChangePeriod(self, period):
        self.period = period