import re
import requests
import json
import pandas as pd
from datetime import datetime


def cbpGetHistoricRates(market='LTC-EUR', granularity=86400, iso8601start='1531216800', iso8601end='1551648800'):
    if not isinstance(market, str):
        raise Exception('Market string input expected')

    if not isinstance(granularity, int):
        raise Exception('Granularity integer input expected')

    granularity_options = [60, 300, 900, 3600, 21600, 86400]
    if not granularity in granularity_options:
        raise Exception(
            'Invalid granularity: 60, 300, 900, 3600, 21600, 86400')

    if not isinstance(iso8601start, str):
        raise Exception('ISO8601 date string input expected')

    if not isinstance(iso8601end, str):
        raise Exception('ISO8601 date string input expected')

    # iso8601 regex
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'

    if len(iso8601start) < 0:
        match_iso8601 = re.compile(regex).match
        if match_iso8601(iso8601start) is None:
            raise Exception('iso8601 start date is invalid')

    if len(iso8601end) < 0:
        match_iso8601 = re.compile(regex).match
        if match_iso8601(iso8601end) is None:
            raise Exception('iso8601 end date is invalid')
    """api = 'https://api.pro.coinbase.com/products/' + market + '/candles?granularity=' + \
          str(granularity) + '&start?' + iso8601start + '&end?' + iso8601end"""

    startTime = datetime.fromtimestamp(int(iso8601start))
    startTime = datetime.strftime(startTime, "%Y-%m-%dT%H:%M:%S")
    endTime = datetime.fromtimestamp(int(iso8601end))
    endTime = datetime.strftime(endTime, "%Y-%m-%dT%H:%M:%S")
    api = "https://api.pro.coinbase.com/products/"+market+"/candles?start="+\
          startTime+"&end="+endTime+"&granularity="+str(granularity)
    print(api)

    resp = requests.get(api)
    if resp.status_code != 200:
        raise Exception('GET ' + api + ' {}'.format(resp.status_code))
    data = {}
    i=0
    for price in reversed(resp.json()):
        # time, low, high, open, close, volume
        i+=1
        #if i<240: continue
        iso8601 = datetime.fromtimestamp(price[0])
        timestamp = datetime.strftime(iso8601, "%d/%m/%Y %H:%M")
        data[timestamp]=(price[0],price[3],price[2],price[1],price[4])
        """ ovo ide         time      Open     High     Low     Close"""
        #data[timestamp] = [price[0],price[3],price[4],price[2],price[1]]
        """ ovo ide         time     Open     close    high     low"""
        #izbačen time i volume jer su nepotrebni?

        """[time, low, high, open, close, volume],
             [0]  [1]  [2]   [3]   [4]    [5]
        [1415398768, 0.32, 4.2, 0.35, 4.2, 12.3]
        samo su time i volume izbačeni
        """
    #with open("historical_data.json", "w") as outfile:
        #json.dump(data, outfile)
    return data

#def cbpGetHistoricRates(market='LTC-EUR', granularity=86400, iso8601start='', iso8601end=''):

if __name__ == '__main__':
    print(cbpGetHistoricRates('BTC-EUR',86400))