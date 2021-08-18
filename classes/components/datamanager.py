import pandas as pd
import matplotlib.dates as mdates
import historical_data as hsd
import json
import os

import csv


def GetData():
    cwd = os.getcwd()
    print(cwd)
    data = pd.read_csv('file.csv')
    data = data.set_index(pd.DatetimeIndex(data["date"].values))
    data["date"] = pd.to_datetime(data['date'])
    data["date"] = data["date"].apply(mdates.date2num)
    return data


def CreateJson(coin="BTC", fiat="EUR", oldcoin="BTC", iso8601start="153121800", iso8601end="1551648800"):
    dic = {"coin": coin, "fiat": fiat, "oldcoin": oldcoin, "iso8601start": iso8601start, "iso8601end": iso8601end}
    with open("data.json", "w+") as jsonFile:
        json.dump(dic, jsonFile)
    hsd.cbpGetHistoricRates()


def CreateJsonMoney(current_money="100",sell_high="120",sell_low="84"):
    dic = {"current_money":sell_high,"sell_high":sell_high,"sell_low":sell_low}
    #print("tu sam",sell_high,sell_high,sell_low)
    with open("data_money.json", "w+") as jsonFile:
        json.dump(dic, jsonFile)


def GetJsonData():
    with open("data.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    return jsonObject

def GetJsonDataMoney():
    with open("data_money.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    return jsonObject


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



