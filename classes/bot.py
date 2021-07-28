from alpaca_trade_api.rest import *

class TradeBot:
    def __init__(self, APIKEY, SECRETKEY):
        self.apikey = APIKEY
        self.secretkey = SECRETKEY
        self.api = REST(APIKEY, SECRETKEY, "https://paper-api.alpaca.markets", api_version='v2')

    # Get the closing price of an asset in desired time and desired time frame (months, days, hours, etc)
    def GetAssetPrice(self, assetName, timeFrame, period = None):
        barset = self.api.get_barset(assetName, timeFrame, limit=period)
        bars = barset[assetName]

        self.values = []
        for bar in bars:
            self.values.append(bar.c)

        return self.values

    def GetUserData(self):
        pass
