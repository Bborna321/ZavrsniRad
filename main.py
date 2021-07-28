from classes.MACD import *
from classes.bot import *
from components.graphs import *



if __name__ == "__main__":
    bot = TradeBot("PK436GOYBL2K7V3E5H9F", "KeB9ZjkwSg2uK3TS5RHdugGiov7cDyWoCaBX9VCh")

    time = 30
    assets = bot.GetAssetPrice('AAPL', 'day', time)
    x = list(range(time))
    test = MACD(assets, 4)
    test.CalculateMovingAverage("EMA")

    graphs = Graphs(test.MACDline, test.signalLine)


