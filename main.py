from alpaca_trade_api.rest import *
from classes.BaseTactic import *
from classes.MACD import *
import json
import pandas as pd

if __name__ == "__main__":
    api = REST("PK436GOYBL2K7V3E5H9F","KeB9ZjkwSg2uK3TS5RHdugGiov7cDyWoCaBX9VCh", "https://paper-api.alpaca.markets", api_version='v2')

    # Get daily price data for AAPL over the last 5 trading days.
    barset = api.get_barset('AAPL', 'day', limit=5)
    aapl_bars = list(barset['AAPL'])



    # o - open    - cijena s kojom je dionica zapocela dan
    # c - closing - Cijena s kojom je dionica zavrsila dan
    # h - high    - Najviša cijena koju je dionica postigla tokom dana
    # l - low     - Najmanja cijena koju je dionica postigla tokom dana
    print(barset)

    # See how much AAPL moved in that timeframe.
    data = aapl_bars[0 : -1].c
    for x in aapl_bars:
        data.append(x.c)

    test = BaseTactic([2,4,6,8], 4)
    test.CalculateMovingAverage()
    print(test.ExponentialMovingAverage, test.SimpleMovingAverage)