class BaseTactic:
    def __init__(self, data, period):
        self.data = data
        self.period = period
        self.day = 0
        self.SimpleMovingAverage = []
        self.ExponentialMovingAverage = []

    def CalculateMovingAverage(self, movingAverage, data=None):
        if data is None:
            data = self.data

        list = []
        if movingAverage == "SMA":
            list = self.__CalculateSimpleAverage(data)
        else:
            list = self.__CalculateExponentialAverage(data, len(data) - 1)
        return list

    # Simple moving average formula:
    # SMA = period sum / N
    # N = number of days in a given period
    # period sum = sum of stocks closing prices in that period
    def __CalculateSimpleAverage(self, data):
        i = 0

        temp = []
        while (len(self.data) - (self.period + i)) >= 0:
            movingAverage = data[len(self.data) - (self.period + i): len(self.data) - i]
            temp.append(sum(movingAverage) / self.period)
            i = i + 1

        temp.reverse()
        return temp

    # Exponential moving average formula:
    # S(t) = a*Y_t + (1-a)*S_{t-1} , t > 1
    # S(t) = Y_t , t = 1
    def __CalculateExponentialAverage(self, data, position):
        k = 2 / (self.period + 1)
        temp = []
        if position == 0:
            temp.append(data[0])
        else:
            temp = temp + self.__CalculateExponentialAverage(data, position - 1)
            temp.append(round(k * data[position] + (1.0 - k) * temp[-1],4))
        return temp

    def ClearMovingAverages(self):
        self.ExponentialMovingAverage = []
        self.SimpleMovingAverage = []
        self.day = 0

    def ChangePeriod(self, period):
        self.period = period
