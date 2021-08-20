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
        self.data['0.0'] = [""] * n
        self.data['23.6'] = [""] * n
        self.data['38.2'] = [""] * n
        self.data['50.0'] = [""] * n
        self.data['61.8'] = [""] * n
        self.data['100.0'] = [""] * n
        self.__SetExtremes(0, ival)
        self.trading_type_1 = False
        self.trading_type_1_prep = False
        self.starting_ival_for_prep = 0

    # Sets global minimum and maximum for each given date
    def __SetExtremes(self, leftValue, rightValue):
        for i in range(rightValue - leftValue):
            if self.data['close'][i + leftValue] < self.mins:
                self.mins = self.data['close'][i + leftValue]
            elif self.data['close'][i + leftValue] > self.maxs:
                self.maxs = self.data['close'][i + leftValue]

        self.data['0.0'][leftValue: rightValue + 1] = [self.maxs] * ((rightValue - leftValue) + 1)
        self.data['100.0'][leftValue: rightValue + 1] = [self.mins] * ((rightValue - leftValue) + 1)
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
        self.data['23.6'][leftValue: rightValue + 1] = [firstLevel] * ((rightValue - leftValue) + 1)
        self.data['38.2'][leftValue: rightValue + 1] = [secondLevel] * ((rightValue - leftValue) + 1)
        self.data['50.0'][leftValue: rightValue + 1] = [thirdLevel] * ((rightValue - leftValue) + 1)
        self.data['61.8'][leftValue: rightValue + 1] = [fourthLevel] * ((rightValue - leftValue) + 1)

        self.mean3 = self.data['close'].ewm(span=3, adjust=False).mean()

    def GetAnimationData(self, leftValue, rightValue):
        if self.__CheckIfExtremeEntered(rightValue):
            self.maxs = 0
            self.mins = 1000000
            self.__SetExtremes(leftValue, rightValue)
        elif self.left:
            self.maxs = 0
            self.mins = 1000000
            self.__SetExtremes(leftValue, rightValue)
        elif self.data['0.0'][rightValue - 1] == "":
            self.maxs = 0
            self.mins = 1000000
            self.__SetExtremes(leftValue, rightValue)
        else:
            self.data['0.0'][rightValue] = str(self.data['0.0'][rightValue - 1])
            self.data['23.6'][rightValue] = str(self.data['23.6'][rightValue - 1])
            self.data['38.2'][rightValue] = str(self.data['38.2'][rightValue - 1])
            self.data['50.0'][rightValue] = str(self.data['50.0'][rightValue - 1])
            self.data['61.8'][rightValue] = str(self.data['61.8'][rightValue - 1])
            self.data['100.0'][rightValue] = str(self.data['100.0'][rightValue - 1])
        self.__CheckIfExtremeLeft(leftValue)

        ap = [
            [self.data['0.0'].iloc[leftValue: rightValue], 'line'],
            [self.data['23.6'].iloc[leftValue: rightValue], 'line'],
            [self.data['38.2'].iloc[leftValue: rightValue], 'line'],
            [self.data['50.0'].iloc[leftValue: rightValue], 'line'],
            [self.data['61.8'].iloc[leftValue: rightValue], 'line'],
            [self.data['100.0'].iloc[leftValue: rightValue], 'line'],
            [self.mean3.iloc[leftValue:rightValue],'line']
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
        newData['0.0'] = [""] * n
        newData['23.6'] = [""] * n
        newData['38.2'] = [""] * n
        newData['50.0'] = [""] * n
        newData['61.8'] = [""] * n
        newData['100.0'] = [""] * n
        self.data = pd.concat([self.data, newData], axis=0)


    def trading_start_signal(self, ival, plotdata):
        if ival < 35:
            return False
        """print(self.mean3[ival])
        print(self.mean3[-3])
        print(self.mean3[-1])
        print(self.data['50.0'][-1])
        print("doljeˇˇˇˇˇˇˇˇ")"""
        # and float(self.mean3[ival]) < float(self.data['50.0'][ival])*1.03\
        # and float(self.mean3[ival]) > float(self.data['50.0'][ival])/1.03:
        if self.starting_ival_for_prep + 2 < ival:
            self.trading_type_1_prep = False
        if (float(self.mean3[ival-3])>float(self.mean3[ival]) or float(self.mean3[ival-5])>float(self.mean3[ival]))\
            and float(self.data['50.0'][ival]) / 1.03 < float(self.mean3[ival]) < float(self.data['50.0'][ival])*1.03:
            self.trading_type_1_prep = True
            self.starting_ival_for_prep = ival
            """print("tu1",float(self.data['50.0'][ival]) / 1.03)
            print("tu2",float(self.mean3[ival]))
            print("tu3",float(self.data['50.0'][ival]) * 1.03)"""
            return False
        if self.trading_type_1_prep and self.mean3[ival]>self.mean3[ival-1]:
            self.trading_type_1 = True
            self.trading_type_1_prep = False
            """print("tu4",self.mean3[ival])
            print("tu5",self.mean3[ival-1])
            print("ODAVDE VRAĆAM TRUE ZA TRADING")"""
            #quit()
            return True


    def trading_stop_signal(self, ival, plotdata):
        #print("tu:",self.data['23.6'][ival],":ut")
        if ival < 35:
            return False
        if  self.trading_type_1:
            if float(self.mean3[ival])>float(self.data['23.6'][ival]):
                self.trading_type_1 = False
                return True
            if float(self.mean3[ival]) < float(self.data['61.8'][ival])*1.05:
                self.trading_type_1 = False
                return True
