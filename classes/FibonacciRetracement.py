from classes.components.datamanager import *
import mplfinance as mpf


class FibonacciRetracement:
    def __init__(self, ax1):
        self.ax1 = ax1
        self.data = GetData()
        self.__SetExtremes()

    # Sets global minimum and maximum for each given date
    def __SetExtremes(self):
        oldMax = 0
        oldMin = 1000000
        oldMaxs = []
        oldMins = []
        for i in range(self.data['close'].values.shape[0]):

            if oldMax < self.data['close'][i] < oldMin:
                oldMax = self.data['close'][i]
                oldMin = self.data['close'][i]
                oldMaxs.append(oldMax)
                oldMins.append(oldMin)
            elif self.data['close'][i] < oldMin:
                oldMin = self.data['close'][i]
                oldMaxs.append(oldMax)
                oldMins.append(oldMin)
            elif self.data['close'][i] > oldMax:
                oldMax = self.data['close'][i]
                oldMaxs.append(oldMax)
                oldMins.append(oldMin)
            else:
                oldMaxs.append(oldMax)
                oldMins.append(oldMin)
        self.data['Maximum price'] = oldMaxs
        self.data['Minimum price'] = oldMins
        self.__SetLevels(oldMaxs, oldMins)

    # First  level: 23.6%
    # Second level: 38.2%
    # Third  level: 50.0%
    # Fourth level: 61.8%
    def __SetLevels(self, oldMaxs, oldMins):
        firstLevels = []
        secondLevels = []
        thirdLevels = []
        fourthLevels = []
        for i in range(len(oldMaxs)):
            difference = oldMaxs[i] - oldMins[i]
            firstLevels.append(oldMaxs[i] - difference * 0.236)
            secondLevels.append(oldMaxs[i] - difference * 0.382)
            thirdLevels.append(oldMaxs[i] - difference * 0.5)
            fourthLevels.append(oldMaxs[i] - difference * 0.618)
        self.data['First level'] = firstLevels
        self.data['Second level'] = secondLevels
        self.data['Third level'] = thirdLevels
        self.data['Fourth level'] = fourthLevels


    def GetAnimationData(self, ival):
        self.ap = [
            [self.data['Maximum price'].iloc[0:ival], 'line'],
            [self.data['First level'].iloc[0:ival], 'line'],
            [self.data['Second level'].iloc[0:ival], 'line'],
            [self.data['Third level'].iloc[0:ival], 'line'],
            [self.data['Fourth level'].iloc[0:ival], 'line'],
            [self.data['Minimum price'].iloc[0:ival], 'line']
        ]
        print(self.ap)
        return self.ap
