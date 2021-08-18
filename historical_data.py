import re
import requests
from datetime import datetime
from global_vars import granularity
from matplotlib.dates import date2num
import json
import csv


def CreateCSV(dicto):
    csv_columns = ["date", "open", "high", "low", "close"]
    csv_file = "file.csv"
    with open(csv_file, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for datas in dicto:
            writer.writerow(datas)


def cbpGetHistoricRates():
    granularity = 86400
    with open("data.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    market = jsonObject["coin"] + "-" + jsonObject["fiat"]
    iso8601start = str(jsonObject['iso8601start'])
    iso8601end = str(jsonObject['iso8601end'])

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
    api = "https://api.pro.coinbase.com/products/" + market + "/candles?start=" + \
          startTime + "&end=" + endTime + "&granularity=" + str(granularity)
    print(api)

    resp = requests.get(api)
    if resp.status_code != 200:
        raise Exception('GET ' + api + ' {}'.format(resp.status_code))
    data = {}
    i = 0

    dict = []
    for price in reversed(resp.json()):
        # time, low, high, open, close, volume
        i += 1
        # if i<240: continue
        iso8601 = datetime.fromtimestamp(price[0])
        timestamp = datetime.strftime(iso8601, "%d/%m/%Y")
        timestamp1 = datetime.strptime(timestamp, "%d/%m/%Y")
        """ ovo ide         time      Open     High     Low     Close"""
        data[timestamp] = (date2num(timestamp1), price[3], price[2], price[1], price[4])
        dict.append({"date": timestamp, "open": price[3], "high": price[2], "low": price[1], "close": price[4]})

    CreateCSV(dict)

    return data
