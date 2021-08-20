from classes.components.datamanager import *

pd.options.mode.chained_assignment = None


class FibonacciRetracement:
    def __init__(self, ax1, ival):
        self.ax1 = ax1
        self.data = GetData()
        self.maxs = 0
        self.mins = 1000000
        self.left = False
        n = len(list(self.data['close'].values))
        self.data['Maximum price'] = [""] * n
        self.data['First level'] = [""] * n
        self.data['Second level'] = [""] * n
        self.data['Third level'] = [""] * n
        self.data['Fourth level'] = [""] * n
        self.data['Minimum price'] = [""] * n
        self.__SetExtremes(0, ival)

    # Sets global minimum and maximum for each given date
    def __SetExtremes(self, leftValue, rightValue):
        for i in range(rightValue - leftValue):
            if self.data['close'][i + leftValue] < self.mins:
                self.mins = self.data['close'][i + leftValue]
            elif self.data['close'][i + leftValue] > self.maxs:
                self.maxs = self.data['close'][i + leftValue]

        self.data['Maximum price'][leftValue: rightValue + 1] = [self.maxs] * ((rightValue - leftValue) + 1)
        self.data['Minimum price'][leftValue: rightValue + 1] = [self.mins] * ((rightValue - leftValue) + 1)
        self.__SetLevels(leftValue, rightValue)

    # First  level: 23.6%
    # Second level: 38.2%
    # Third  level: 50.0%
    # Fourth level: 61.8%
    def __SetLevels(self, leftValue, rightValue):
        difference = self.maxs - self.mins
        firstLevel = self.maxs - difference * 0.236
        secondLevel = self.maxs - difference * 0.382
        thirdLevel = self.maxs - difference * 0.5
        fourthLevel = self.maxs - difference * 0.618
        self.data['First level'][leftValue: rightValue + 1] = [firstLevel] * ((rightValue - leftValue) + 1)
        self.data['Second level'][leftValue: rightValue + 1] = [secondLevel] * ((rightValue - leftValue) + 1)
        self.data['Third level'][leftValue: rightValue + 1] = [thirdLevel] * ((rightValue - leftValue) + 1)
        self.data['Fourth level'][leftValue: rightValue + 1] = [fourthLevel] * ((rightValue - leftValue) + 1)

    def GetAnimationData(self, leftValue, rightValue):
        if self.__CheckIfExtremeEntered(rightValue):
            self.maxs = 0
            self.mins = 1000000
            self.__SetExtremes(leftValue, rightValue)
        elif self.left:
            self.maxs = 0
            self.mins = 1000000
            self.__SetExtremes(leftValue, rightValue)
        elif self.data['Maximum price'][rightValue - 1] == "":
            self.maxs = 0
            self.mins = 1000000
            self.__SetExtremes(leftValue, rightValue)
        else:
            self.data['Maximum price'][rightValue] = str(self.data['Maximum price'][rightValue - 1])
            self.data['First level'][rightValue] = str(self.data['First level'][rightValue - 1])
            self.data['Second level'][rightValue] = str(self.data['Second level'][rightValue - 1])
            self.data['Third level'][rightValue] = str(self.data['Third level'][rightValue - 1])
            self.data['Fourth level'][rightValue] = str(self.data['Fourth level'][rightValue - 1])
            self.data['Minimum price'][rightValue] = str(self.data['Minimum price'][rightValue - 1])
        self.__CheckIfExtremeLeft(leftValue)

        ap = [
            [self.data['Maximum price'].iloc[leftValue: rightValue], 'line'],
            [self.data['First level'].iloc[leftValue: rightValue], 'line'],
            [self.data['Second level'].iloc[leftValue: rightValue], 'line'],
            [self.data['Third level'].iloc[leftValue: rightValue], 'line'],
            [self.data['Fourth level'].iloc[leftValue: rightValue], 'line'],
            [self.data['Minimum price'].iloc[leftValue: rightValue], 'line']
        ]
        return ap

    def __CheckIfExtremeLeft(self, leftValue):
        closing = self.data['close'][leftValue]
        left = closing == self.maxs or closing == self.mins
        self.left = left

    def __CheckIfExtremeEntered(self, rightValue):
        closing = self.data['close'][rightValue - 1]
        if closing < self.mins:
            self.mins = closing
            return True
        elif closing > self.maxs:
            self.maxs = closing
            return True
        else:
            return False

    def UpdateData(self, newData):
        n = len(list(newData['close'].values))
        newData['Maximum price'] = [""] * n
        newData['First level'] = [""] * n
        newData['Second level'] = [""] * n
        newData['Third level'] = [""] * n
        newData['Fourth level'] = [""] * n
        newData['Minimum price'] = [""] * n
        self.data = pd.concat([self.data, newData], axis=0)
