import historical_data as hsd

class RSI:
    def __init__(self):
        self.data = hsd.cbpGetHistoricRates()
        print(self.data.keys())