from classes.components.datamanager import *

pd.options.mode.chained_assignment = None


class FibonacciRetracement:
    def __init__(self, ival):
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
        self.mean3 = self.data['close'].ewm(span=3, adjust=False).mean()
        self.trading_type_1 = False
        self.trading_type_1_prep = False
        self.starting_ival_for_prep_1 = 0

        self.trading_type_2 = False
        self.trading_type_2_prep = False
        self.starting_ival_for_prep_2 = 0

        self.at_least_one = 0

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

    def SetData(self, leftValue, rightValue):
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

    def GetAnimationData(self, leftValue, rightValue):
        self.SetData(leftValue, rightValue)

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
        self.mean3 = self.data['close'].ewm(span=3, adjust=False).mean()


    """def trading_start_signal(self, ival, plotdata):
        if self.trading_type_1 or self.trading_type_2:
            return False
        print("tipovi",self.trading_type_1, self.trading_type_2)
        self.trading_start_signal_go(ival, plotdata)"""

    def trading_start_signal(self, ival, money_manager):
        ival = ival -1
        if ival < 35:
            return False

        if self.starting_ival_for_prep_1 + 2 < ival:
            self.trading_type_1_prep = False

        dummy_diff = float(self.data['38.2'][ival]) - float(self.data['50.0'][ival])
        dummy_temp_border = float(self.data['50.0'][ival]) + dummy_diff * 0.2
        dummy_diff_low = float(self.data['50.0'][ival]) - float(self.data['61.8'][ival])
        dummy_temp_border_low = float(self.data['61.8'][ival]) * dummy_diff_low*0.9
        if (float(self.mean3[ival-3]) > float(self.mean3[ival]) or float(self.mean3[ival-5]) > float(self.mean3[ival]))\
            and dummy_temp_border_low < float(self.mean3[ival]) < dummy_temp_border:
            self.trading_type_1_prep = True
            self.starting_ival_for_prep_1 = ival
            return False
        if self.trading_type_1_prep and self.mean3[ival]>self.mean3[ival-1]:
            self.trading_type_1 = True
            self.trading_type_1_prep = False
            self.trading_type_2_prep = False
            self.at_least_one = ival
            return True

        dummy_diff = float(self.data['38.2'][ival]) - float(self.data['50.0'][ival])
        dummy_temp_border = float(self.data['50.0'][ival]) + dummy_diff*0.8
        dummy_diff_high = float(self.data['23.6'][ival]) - float(self.data['38.2'][ival])
        dummy_temp_border_high =  float(self.data['38.2'][ival]) + dummy_diff_high*0.8
        if (float(self.mean3[ival-3])<float(self.mean3[ival]) or float(self.mean3[ival-5])<float(self.mean3[ival]))\
            and dummy_temp_border < float(self.mean3[ival]) < dummy_temp_border_high:
            #and float(self.data['38.2'][ival]) / 1.031 < float(self.mean3[ival]) < float(self.data['38.2'][ival]) * 1.031:
            self.trading_type_2 = True
            self.trading_type_2_prep = False
            self.trading_type_1_prep = False
            self.at_least_one = ival

            return True

    def trading_stop_signal(self, ival, plotdata):
        ival = ival - 1
        if self.at_least_one + 2 > ival or\
                ival < 35:
            return False
        """print("jedan:",self.trading_type_1)
        print("dva:",self.trading_type_2)"""

        if self.trading_type_1:
            if float(self.mean3[ival]) > float(self.data['23.6'][ival]):
                self.trading_type_1 = False
                return True
            dummy_diff = float(self.data['50.0'][ival]) - float(self.data['61.8'][ival])
            dummy_temp_border = float(self.data['61.8'][ival]) + dummy_diff * 0.3
            if float(self.mean3[ival]) < dummy_temp_border:
                self.trading_type_1 = False
                return True
        elif self.trading_type_2:
            dummy_diff = float(self.data['0.0'][ival]) - float(self.data['23.6'][ival])
            dummy_temp_border = float(self.data['23.6'][ival]) + dummy_diff * 0.65
            if float(self.mean3[ival]) > dummy_temp_border:
                self.trading_type_2=False
                #print("izašo iz prvog razloga")
                return True
            if float(self.mean3[ival]) < float(self.data['50.0'][ival]):
                self.trading_type_2 = False
                #print("izašo iz drugog razloga")
                return True
        return False
