import pandas as pd
import matplotlib.dates as mdates
import historical_data as hsd
import json
import csv


def GetData():
    data = pd.read_csv('file.csv')
    data = data.set_index(pd.DatetimeIndex(data["date"].values))
    data["date"] = pd.to_datetime(data['date'])
    data["date"] = data["date"].apply(mdates.date2num)
    return data


def CreateJson(coin="BTC", fiat="EUR", oldcoin="BTC", iso8601start="153121800", iso8601end="1551648800"):
    dic = {"coin": coin, "fiat": fiat, "oldcoin": oldcoin, "iso8601start": iso8601start, "iso8601end": iso8601end}
    with open("data.json", "w+") as jsonFile:
        json.dump(dic, jsonFile)


def ChangeCoing(newcoin_var):
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["oldcoin"] = data["coin"]
    data["coin"] = newcoin_var.get()

    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    hsd.cbpGetHistoricRates()

    data = GetData()
    return data



